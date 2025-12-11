import os
import subprocess
import threading
import time
import platform
import glob
import secrets
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
from functools import wraps
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Secure SECRET_KEY: Use environment variable or generate secure random key
app.config['SECRET_KEY'] = os.environ.get('WIFI_CRACKER_SECRET_KEY') or secrets.token_hex(32)

# Authentication configuration
# Set WIFI_CRACKER_PASSWORD environment variable to enable authentication
# Set WIFI_CRACKER_HOST to '0.0.0.0' to enable network access (Default: '127.0.0.1' / localhost only)
AUTH_PASSWORD = os.environ.get('WIFI_CRACKER_PASSWORD')
RESTRICT_TO_LOCALHOST = os.environ.get('WIFI_CRACKER_HOST', '127.0.0.1') == '127.0.0.1'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('temp', exist_ok=True)
os.makedirs('wordlists', exist_ok=True)

# Store job status
jobs = {}

# Authentication decorator
def check_auth(username, password):
    """Check if username/password combination is valid"""
    # Simple single-user authentication
    # Username is ignored, only password is checked
    if AUTH_PASSWORD:
        return password == AUTH_PASSWORD
    return True  # No authentication if password not set

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Authentication required. Please provide the password.', 401,
        {'WWW-Authenticate': 'Basic realm="WiFi Cracker Login Required"'})

def requires_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if AUTH_PASSWORD:
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated

# Common wordlist for quick testing
COMMON_PASSWORDS = [
    "password", "12345678", "123456789", "1234567890", "qwerty", "abc123",
    "password123", "admin", "letmein", "welcome", "monkey", "1234567",
    "123456", "password1", "qwerty123", "admin123", "welcome123"
]

ALLOWED_EXTENSIONS_PCAP = {'pcap', 'cap', 'pcapng'}
ALLOWED_EXTENSIONS_WORDLIST = {'txt'}

def check_external_tool(tool_name):
    """Check if an external tool is available in PATH or local tools directory"""
    import shutil
    
    # First check local tools directory (for portable installations)
    local_tools_dir = os.path.join(os.path.dirname(__file__), 'tools', 'bin')
    if os.path.exists(local_tools_dir):
        local_tool = os.path.join(local_tools_dir, tool_name)
        if platform.system() == 'Windows':
            local_tool_exe = local_tool + '.exe'
            if os.path.exists(local_tool_exe):
                return local_tool_exe
        if os.path.exists(local_tool):
            return local_tool
    
    # Check system PATH
    tool_path = shutil.which(tool_name)
    if tool_path:
        return tool_path
    # Try with .exe extension on Windows
    if platform.system() == 'Windows':
        tool_path = shutil.which(tool_name + '.exe')
        if tool_path:
            return tool_path
    return None

def get_tool_command(tool_name):
    """Get the command to run for a tool, handling Windows .exe extension and WSL"""
    if platform.system() == 'Windows':
        # Try .exe extension first on Windows
        exe_path = check_external_tool(tool_name + '.exe')
        if exe_path:
            return exe_path
        # Try WSL if tool not found natively
        tool_path = check_external_tool(tool_name)
        if not tool_path:
            # Check if WSL is available and tool exists in WSL
            try:
                result = subprocess.run(['wsl', 'which', tool_name], capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and result.stdout.strip():
                    # Return WSL command wrapper
                    return ['wsl', tool_name]
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
    tool_path = check_external_tool(tool_name)
    if tool_path:
        return tool_path
    # Return original name if not found (will fail with better error message)
    return tool_name

def windows_to_wsl_path(windows_path):
    r"""Convert a Windows path to a WSL path (e.g. C:\Users -> /mnt/c/Users)"""
    windows_path = os.path.abspath(windows_path)
    drive, tail = os.path.splitdrive(windows_path)
    drive = drive.lower().replace(':', '')
    # Convert backslashes to forward slashes and prepend WSL mount point
    # Handle both separator types just in case
    tail = tail.replace('\\', '/')
    return f'/mnt/{drive}{tail}'

def allowed_file(filename, file_type='pcap'):
    if file_type == 'pcap':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PCAP
    elif file_type == 'wordlist':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_WORDLIST
    return False

def run_dictionary_attack(job_id, pcap_path, wordlist_path):
    """Run dictionary attack in background thread"""
    try:
        # Check if required tools are available
        hcxpcapngtool_cmd = get_tool_command('hcxpcapngtool')
        hashcat_cmd = get_tool_command('hashcat')
        
        if hcxpcapngtool_cmd == 'hcxpcapngtool' and not check_external_tool('hcxpcapngtool') and not check_external_tool('hcxpcapngtool.exe'):
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = 'hcxpcapngtool not found. Please install hcxtools (in Windows PATH or WSL).'
            return
        
        if hashcat_cmd == 'hashcat' and not check_external_tool('hashcat') and not check_external_tool('hashcat.exe'):
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = 'hashcat not found. Please install hashcat (in Windows PATH or WSL).'
            return
        
        jobs[job_id]['status'] = 'processing'
        jobs[job_id]['message'] = 'Converting PCAP to hc22000 format...'
        
        # Validate PCAP file exists
        if not os.path.exists(pcap_path):
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = f'PCAP file not found: {pcap_path}'
            return
        
        if not os.path.isfile(pcap_path):
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = f'Invalid PCAP file path: {pcap_path}'
            return
        
        # Ensure temp directory exists
        temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        

        # Convert PCAP to hc22000
        hc22000_file = os.path.join(temp_dir, f'{job_id}.hc22000')
        try:
            # Handle WSL commands (list format) vs regular commands (string)
            if isinstance(hcxpcapngtool_cmd, list):
                # WSL command: ['wsl', 'hcxpcapngtool']
                # Convert Windows path to WSL path manually to avoid escaping issues
                if platform.system() == 'Windows':
                    wsl_hc22000 = windows_to_wsl_path(hc22000_file)
                    wsl_pcap = windows_to_wsl_path(pcap_path)
                    
                    cmd = hcxpcapngtool_cmd + ['-o', wsl_hc22000, wsl_pcap]
                else:
                    cmd = hcxpcapngtool_cmd + ['-o', hc22000_file, pcap_path]
            else:
                cmd = [hcxpcapngtool_cmd, '-o', hc22000_file, pcap_path]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
        except FileNotFoundError:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = f'hcxpcapngtool not found. Please install hcxtools. See docs/INSTALL_TOOLS.md for installation instructions.'
            return
        except subprocess.TimeoutExpired:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = 'PCAP conversion timed out after 5 minutes'
            return
        
        if result.returncode != 0:
            jobs[job_id]['status'] = 'error'
            error_msg = result.stderr if result.stderr else result.stdout
            # Include command and paths in error for debugging
            cmd_str = ' '.join(cmd) if isinstance(cmd, list) else str(cmd)
            jobs[job_id]['message'] = f'Error converting PCAP: {error_msg}\nCommand: {cmd_str}\nPCAP path: {pcap_path}'
            return
        
        jobs[job_id]['message'] = 'Running hashcat dictionary attack...'
        
        # Run hashcat attack
        try:
            # Handle WSL commands vs regular commands
            if isinstance(hashcat_cmd, list):
                if platform.system() == 'Windows':
                    wsl_hc22000 = windows_to_wsl_path(hc22000_file)
                    wsl_wordlist = windows_to_wsl_path(wordlist_path)
                    
                    cmd = hashcat_cmd + ['-m', '22000', wsl_hc22000, wsl_wordlist, '--potfile-disable']
                else:
                    cmd = hashcat_cmd + ['-m', '22000', hc22000_file, wordlist_path, '--potfile-disable']
            else:
                cmd = [hashcat_cmd, '-m', '22000', hc22000_file, wordlist_path, '--potfile-disable']
            
            hashcat_result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
        except FileNotFoundError:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = f'hashcat not found. Please install hashcat. See docs/INSTALL_TOOLS.md for installation instructions.'
            return
        
        # Check if hashcat found the password by running --show
        try:
            if isinstance(hashcat_cmd, list):
                if platform.system() == 'Windows':
                    wsl_hc22000 = subprocess.run(['wsl', 'wslpath', '-a', os.path.abspath(hc22000_file)], 
                                                capture_output=True, text=True, timeout=5).stdout.strip()
                    cmd = hashcat_cmd + ['-m', '22000', wsl_hc22000, '--show']
                else:
                    cmd = hashcat_cmd + ['-m', '22000', hc22000_file, '--show']
            else:
                cmd = [hashcat_cmd, '-m', '22000', hc22000_file, '--show']
            
            show_result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
        except FileNotFoundError:
            jobs[job_id]['status'] = 'error'
            jobs[job_id]['message'] = f'hashcat not found. Please install hashcat. See docs/INSTALL_TOOLS.md for installation instructions.'
            return
        
        # Parse hashcat --show output to get password
        if show_result.returncode == 0 and show_result.stdout.strip():
            # Format: hash:password (hc22000 format)
            output_lines = show_result.stdout.strip().split('\n')
            for line in output_lines:
                if ':' in line:
                    # Split by colon, password is after the last colon
                    parts = line.split(':')
                    if len(parts) >= 2:
                        # In hc22000 format: *hash*:password
                        password = parts[-1].strip()
                        if password:
                            jobs[job_id]['status'] = 'success'
                            jobs[job_id]['password'] = password
                            jobs[job_id]['message'] = 'Password found!'
                            
                            # Cleanup
                            if os.path.exists(hc22000_file):
                                os.remove(hc22000_file)
                            return
        
        jobs[job_id]['status'] = 'failed'
        jobs[job_id]['message'] = 'Password not found in wordlist'
        
        # Cleanup
        if os.path.exists(hc22000_file):
            os.remove(hc22000_file)
            
    except subprocess.TimeoutExpired:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['message'] = 'Operation timed out'
    except FileNotFoundError as e:
        jobs[job_id]['status'] = 'error'
        if 'hcxpcapngtool' in str(e) or 'hcxpcapngtool.exe' in str(e):
            jobs[job_id]['message'] = 'hcxpcapngtool not found. Please install hcxtools and ensure it is in your PATH. See docs/INSTALL_TOOLS.md for installation instructions.'
        elif 'hashcat' in str(e) or 'hashcat.exe' in str(e):
            jobs[job_id]['message'] = 'hashcat not found. Please install hashcat and ensure it is in your PATH. See docs/INSTALL_TOOLS.md for installation instructions.'
        else:
            jobs[job_id]['message'] = f'External tool not found: {str(e)}. Please check your installation.'
    except Exception as e:
        jobs[job_id]['status'] = 'error'
        jobs[job_id]['message'] = f'Error: {str(e)}'
    finally:
        # Cleanup uploaded files
        try:
            if os.path.exists(pcap_path):
                os.remove(pcap_path)
            if os.path.exists(wordlist_path):
                os.remove(wordlist_path)
        except (OSError, IOError) as e:
            # Log but don't fail if cleanup fails
            pass

@app.route('/')
@requires_auth
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
@requires_auth
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
@requires_auth
def upload_files():
    if 'pcap_file' not in request.files or 'wordlist_file' not in request.files:
        return jsonify({'error': 'Missing files'}), 400
    
    pcap_file = request.files['pcap_file']
    wordlist_file = request.files['wordlist_file']
    
    if pcap_file.filename == '' or wordlist_file.filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    if not allowed_file(pcap_file.filename, 'pcap'):
        return jsonify({'error': 'Invalid PCAP file format'}), 400
    
    if not allowed_file(wordlist_file.filename, 'wordlist'):
        return jsonify({'error': 'Invalid wordlist file format'}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save files
    pcap_filename = secure_filename(f'{job_id}_{pcap_file.filename}')
    wordlist_filename = secure_filename(f'{job_id}_{wordlist_file.filename}')
    
    pcap_path = os.path.join(app.config['UPLOAD_FOLDER'], pcap_filename)
    wordlist_path = os.path.join(app.config['UPLOAD_FOLDER'], wordlist_filename)
    
    pcap_file.save(pcap_path)
    wordlist_file.save(wordlist_path)
    
    # Initialize job status
    jobs[job_id] = {
        'status': 'queued',
        'message': 'Job queued...',
        'password': None
    }
    
    # Start attack in background thread
    thread = threading.Thread(
        target=run_dictionary_attack,
        args=(job_id, pcap_path, wordlist_path)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'job_id': job_id, 'message': 'Files uploaded successfully'})

@app.route('/status/<job_id>')
@requires_auth
def get_status(job_id):
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(jobs[job_id])

def detect_flipper_using_cli_tools():
    """Detect Flipper Zero using the Python CLI tools (proper method)
    Uses flipper_serial_by_name() and connection method from rpc.py/clipper.py
    """
    flipper_devices = []
    
    try:
        import sys
        import os
        cli_tools_path = os.path.join(os.path.dirname(__file__), 'tools')
        if not os.path.exists(cli_tools_path):
            return []
        
        # Add tools to path (same as CLI tools do)
        sys.path.insert(0, cli_tools_path)
        
        try:
            import serial
            import serial.tools.list_ports
            
            # Import CLI helpers (exactly like rpc.py does)
            try:
                from src.helpers import flipper_serial_by_name
            except ImportError:
                flipper_serial_by_name = None
            
            # Try to import ProtoFlipper (exactly like rpc.py does)
            try:
                from flipperzero_protobuf_py.flipper_protobuf import ProtoFlipper
                has_protobuf = True
            except ImportError:
                has_protobuf = False
            
            # Method 1: Try all COM ports directly (Windows) or use flipper_serial_by_name (Linux/Mac)
            # On Windows, we need to try COM ports directly since flipper_serial_by_name() 
            # only checks if path exists (and COM ports don't exist as files)
            if platform.system() == 'Windows':
                # Try all COM ports directly (like CLI tools when you pass COM port name)
                ports = serial.tools.list_ports.comports()
                for port in ports:
                    port_desc = (port.description or '').lower()
                    port_hwid = (getattr(port, 'hwid', '') or '').lower()
                    
                    # Skip Bluetooth and other non-serial ports
                    if 'bluetooth' in port_desc:
                        continue
                    
                    # Try connecting directly to this COM port
                    try:
                        # Connect using EXACT method from rpc.py/clipper.py (lines 87-97)
                        flipper = serial.Serial(port.device, timeout=1)
                        flipper.baudrate = 230400
                        flipper.flushOutput()
                        flipper.flushInput()
                        
                        # Wait for CLI prompt (exactly like rpc.py line 94)
                        # Set timeout for reading prompt, then set to None for blocking reads
                        try:
                            flipper.timeout = 3  # Give it 3 seconds to respond
                            prompt = flipper.read_until(b'>: ')
                            flipper.timeout = None  # Set back to blocking (like rpc.py line 92)
                            
                            if b'>: ' in prompt:
                                # Got prompt! Start RPC session (exactly like rpc.py line 96)
                                flipper.write(b"start_rpc_session\r")
                                flipper.read_until(b'\n')
                                
                                # Verify with ping (exactly like rpc.py line 16)
                                if has_protobuf:
                                    try:
                                        proto = ProtoFlipper(flipper)
                                        ping_result = proto.cmd_system_ping()
                                        if ping_result == b'\xde\xad\xbe\xef':
                                            flipper_devices.append({
                                                'path': port.device,
                                                'method': 'python_cli',
                                                'device': port.device,
                                                'description': port.description or 'Unknown',
                                                'hwid': port_hwid,
                                                'verified': True
                                            })
                                            flipper.close()
                                            continue
                                    except Exception as e:
                                        # Ping failed, but RPC session started - likely Flipper
                                        flipper_devices.append({
                                            'path': port.device,
                                            'method': 'python_cli',
                                            'device': port.device,
                                            'description': port.description or 'Unknown',
                                            'hwid': port_hwid,
                                            'verified': False,
                                            'note': f'RPC session started (ping error: {str(e)})'
                                        })
                                        flipper.close()
                                        continue
                                else:
                                    # ProtoFlipper not available, but RPC session started
                                    # This is very likely a Flipper Zero
                                    flipper_devices.append({
                                        'path': port.device,
                                        'method': 'python_cli',
                                        'device': port.device,
                                        'description': port.description or 'Unknown',
                                        'hwid': port_hwid,
                                        'verified': False,
                                        'note': 'RPC session started (protobuf not available)'
                                    })
                                    flipper.close()
                                    continue
                        except Exception as e:
                            # Timeout or no prompt - not a Flipper Zero
                            flipper.close()
                            pass
                    except Exception:
                        # Can't open port - skip it
                        pass
            
            # Method 2: For Linux/Mac, use flipper_serial_by_name() with common names
            # (On Windows, we already tried all COM ports in Method 1)
            if platform.system() != 'Windows' and flipper_serial_by_name:
                # Try common Flipper names (like "Lotak" in README examples)
                test_names = ['Flipper', 'flip', 'Lotak']
                
                for name in test_names:
                    flipper = None
                    try:
                        serial_path = flipper_serial_by_name(name)
                        if serial_path and serial_path != '' and os.path.exists(serial_path):
                            # Connect using EXACT method from rpc.py/clipper.py
                            flipper = serial.Serial(serial_path, timeout=1)
                            flipper.baudrate = 230400
                            flipper.flushOutput()
                            flipper.flushInput()
                            flipper.timeout = None
                            
                            flipper.read_until(b'>: ')
                            flipper.write(b"start_rpc_session\r")
                            flipper.read_until(b'\n')
                            
                            if has_protobuf:
                                try:
                                    proto = ProtoFlipper(flipper)
                                    if proto.cmd_system_ping() == b'\xde\xad\xbe\xef':
                                        flipper_devices.append({
                                            'path': serial_path,
                                            'method': 'python_cli',
                                            'device': serial_path,
                                            'verified': True
                                        })
                                        flipper.close()
                                        flipper = None
                                        continue
                                except Exception:
                                    pass
                            
                            flipper_devices.append({
                                'path': serial_path,
                                'method': 'python_cli',
                                'device': serial_path,
                                'verified': has_protobuf
                            })
                            flipper.close()
                            flipper = None
                    except Exception:
                        # Ensure port is closed even if exception occurs
                        if flipper is not None:
                            try:
                                flipper.close()
                            except Exception:
                                pass
                        pass
                        
        except ImportError as e:
            pass
        except Exception as e:
            pass
            
    except Exception as e:
        pass
    
    return flipper_devices

@app.route('/flipper/detect')
@requires_auth
def detect_flipper():
    """Detect Flipper Zero connected via USB using multiple methods"""
    flipper_paths = []
    detection_methods = []
    
    # Method 1: Use Python CLI tools (proper detection)
    cli_devices = detect_flipper_using_cli_tools()
    if cli_devices:
        detection_methods.append('python_cli')
        flipper_paths.extend(cli_devices)
    
    # Method 1b: Try official Flipper CLI tool (if installed)
    try:
        result = subprocess.run(
            ['flipper-cli', 'info'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            detection_methods.append('official_cli')
            flipper_paths.append({
                'path': '/ext/apps_data/marauder/pcaps',
                'method': 'official_cli',
                'device': 'flipper-cli'
            })
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    except Exception:
        pass
    
    # Method 2: Fallback - Check mounted drives (only if no serial connection found)
    if not flipper_paths:
        if platform.system() == 'Windows':
            for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                path = f"{drive}:\\"
                if os.path.exists(path):
                    # Check multiple possible paths
                    possible_paths = [
                        os.path.join(path, "ext", "apps_data", "marauder", "pcaps"),
                        os.path.join(path, "apps_data", "marauder", "pcaps"),
                        os.path.join(path, "marauder", "pcaps"),
                    ]
                    for flipper_path in possible_paths:
                        if os.path.exists(flipper_path):
                            flipper_paths.append({
                                'path': flipper_path,
                                'drive': drive,
                                'method': 'mounted_drive'
                            })
                            detection_methods.append('mounted_drive')
                            break
        else:
            # Linux/Mac - check common mount points
            common_paths = [
                "/media/flipper/ext/apps_data/marauder/pcaps",
                "/mnt/flipper/ext/apps_data/marauder/pcaps",
                "/Volumes/FLIPPER/ext/apps_data/marauder/pcaps",
                os.path.expanduser("~/flipper/ext/apps_data/marauder/pcaps")
            ]
            for path in common_paths:
                if os.path.exists(path):
                    flipper_paths.append({
                        'path': path,
                        'method': 'mounted_drive'
                    })
                    detection_methods.append('mounted_drive')
    
    # Get debug info
    debug_info = {}
    if platform.system() == 'Windows':
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            debug_info['ports_scanned'] = len(ports)
            debug_info['port_list'] = [{'device': p.device, 'description': p.description} for p in ports[:5]]  # First 5
        except (ImportError, Exception) as e:
            # Serial tools not available or error listing ports
            pass
    
    return jsonify({
        'found': len(flipper_paths) > 0,
        'paths': flipper_paths,
        'methods': list(set(detection_methods)),
        'debug': debug_info
    })

@app.route('/flipper/pcaps')
@requires_auth
def list_flipper_pcaps():
    """List PCAP files on Flipper Zero"""
    flipper_path = request.args.get('path')
    method = request.args.get('method', 'mounted_drive')
    
    pcap_files = []
    
    # Method 1: Using Flipper CLI (official or Python-based)
    if method in ['cli', 'official_cli', 'python_cli', 'com_port']:
        # For Python CLI and COM port detection, we need mounted drive for file access
        # The detection found the device, but file access requires mounted SD card
        if method in ['python_cli', 'com_port']:
            # Try to find mounted drive that corresponds to this device
            # Check all drives for PCAP files
            if platform.system() == 'Windows':
                for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    path = f"{drive}:\\"
                    if os.path.exists(path):
                        possible_paths = [
                            os.path.join(path, "ext", "apps_data", "marauder", "pcaps"),
                            os.path.join(path, "apps_data", "marauder", "pcaps"),
                            os.path.join(path, "marauder", "pcaps"),
                        ]
                        for pcap_path in possible_paths:
                            if os.path.exists(pcap_path):
                                # Found mounted drive with PCAPs
                                for ext in ['*.pcap', '*.cap', '*.pcapng']:
                                    files = glob.glob(os.path.join(pcap_path, ext))
                                    for f in files:
                                        try:
                                            stat = os.stat(f)
                                            pcap_files.append({
                                                'name': os.path.basename(f),
                                                'path': f,
                                                'size': stat.st_size,
                                                'modified': stat.st_mtime,
                                                'method': 'mounted_drive'
                                            })
                                        except (OSError, IOError) as e:
                                            # Skip files that can't be accessed
                                            pass
                                break
                        if pcap_files:
                            break
            return jsonify({
                'files': sorted(pcap_files, key=lambda x: x.get('modified', 0), reverse=True),
                'method': 'mounted_drive',
                'path': flipper_path,
                'note': 'Device detected via serial, files accessed via mounted SD card'
            })
        
        # Official CLI method
        try:
            result = subprocess.run(
                ['flipper-cli', 'storage', 'list', flipper_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Parse CLI output to get file list
                for line in result.stdout.split('\n'):
                    if any(ext in line.lower() for ext in ['.pcap', '.cap', '.pcapng']):
                        # Extract filename from CLI output
                        filename = line.strip().split()[-1] if line.strip() else None
                        if filename:
                            pcap_files.append({
                                'name': filename,
                                'path': f"{flipper_path}/{filename}",
                                'size': 0,  # CLI doesn't always provide size
                                'modified': 0,
                                'method': 'cli'
                            })
        except Exception as e:
            return jsonify({'error': f'CLI error: {str(e)}'}), 500
    
    # Method 2: Using mounted drive (file system)
    elif method == 'mounted_drive' and flipper_path and os.path.exists(flipper_path):
        for ext in ['*.pcap', '*.cap', '*.pcapng']:
            files = glob.glob(os.path.join(flipper_path, ext))
            for f in files:
                try:
                    stat = os.stat(f)
                    pcap_files.append({
                        'name': os.path.basename(f),
                        'path': f,
                        'size': stat.st_size,
                        'modified': stat.st_mtime,
                        'method': 'mounted_drive'
                    })
                except (OSError, IOError) as e:
                    # Skip files that can't be accessed
                    pass
    
    # Method 3: Serial port - would need custom implementation
    elif method == 'serial':
        return jsonify({
            'error': 'Serial port file access not yet implemented. Please use qFlipper or mount the SD card.',
            'files': []
        }), 501
    
    if not pcap_files and flipper_path:
        return jsonify({
            'error': 'No PCAP files found or path not accessible',
            'path': flipper_path,
            'method': method,
            'files': []
        }), 404
    
    # Sort by modified time (newest first)
    pcap_files.sort(key=lambda x: x.get('modified', 0), reverse=True)
    
    return jsonify({
        'files': pcap_files,
        'method': method,
        'path': flipper_path
    })

@app.route('/flipper/download')
@requires_auth
def download_flipper_pcap():
    """Download PCAP file from Flipper Zero"""
    file_path = request.args.get('path')
    
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
        
    # Security Check: Prevent LFI/Arbitrary File Read
    # 1. Validate extension
    file_path_lower = file_path.lower()
    if not (file_path_lower.endswith('.pcap') or 
            file_path_lower.endswith('.cap') or 
            file_path_lower.endswith('.pcapng')):
        return jsonify({'error': 'Security error: Invalid file type'}), 403
        
    # 2. Check existence
    exists = os.path.exists(file_path)
    
    if not exists:
        return jsonify({'error': 'File not found'}), 404
        
    # 3. Ensure it's a file, not a directory
    if not os.path.isfile(file_path):
        return jsonify({'error': 'Invalid path'}), 400
    
    # Copy to uploads folder with unique name
    filename = os.path.basename(file_path)
    job_id = str(uuid.uuid4())
    dest_filename = secure_filename(f'{job_id}_{filename}')
    dest_path = os.path.join(app.config['UPLOAD_FOLDER'], dest_filename)
    
    import shutil
    try:
        shutil.copy2(file_path, dest_path)
    except Exception as e:
        return jsonify({'error': f'Copy failed: {str(e)}'}), 500
    
    return jsonify({
        'success': True,
        'filename': dest_filename,
        'original_name': filename,
        'path': dest_path,
        'message': 'File copied successfully'
    })

@app.route('/wordlists/common')
@requires_auth
def get_common_wordlist():
    """Generate a common passwords wordlist"""
    wordlist_path = os.path.join('wordlists', 'common_passwords.txt')
    with open(wordlist_path, 'w') as f:
        for pwd in COMMON_PASSWORDS:
            f.write(pwd + '\n')
    
    return jsonify({
        'success': True,
        'path': wordlist_path,
        'count': len(COMMON_PASSWORDS)
    })

@app.route('/wordlists/<filename>')
@requires_auth
def serve_wordlist(filename):
    """Serve wordlist files"""
    return send_from_directory('wordlists', filename)

@app.route('/wordlists/list')
@requires_auth
def list_wordlists():
    """List available wordlists"""
    wordlists = []
    wordlist_dir = 'wordlists'
    
    if os.path.exists(wordlist_dir):
        for file in os.listdir(wordlist_dir):
            if file.endswith('.txt'):
                file_path = os.path.join(wordlist_dir, file)
                stat = os.stat(file_path)
                wordlists.append({
                    'name': file,
                    'path': file_path,
                    'size': stat.st_size
                })
    
    return jsonify({'wordlists': wordlists})

@app.route('/check/tools')
@requires_auth
def check_tools():
    """Check if required external tools are installed"""
    import shutil
    tools_status = {}
    
    # Check hcxpcapngtool
    hcxpcapngtool_path = check_external_tool('hcxpcapngtool')
    if not hcxpcapngtool_path and platform.system() == 'Windows':
        hcxpcapngtool_path = check_external_tool('hcxpcapngtool.exe')
    tools_status['hcxpcapngtool'] = {
        'installed': hcxpcapngtool_path is not None,
        'path': hcxpcapngtool_path or 'Not found in PATH'
    }
    
    # Check hashcat
    hashcat_path = check_external_tool('hashcat')
    if not hashcat_path and platform.system() == 'Windows':
        hashcat_path = check_external_tool('hashcat.exe')
    tools_status['hashcat'] = {
        'installed': hashcat_path is not None,
        'path': hashcat_path or 'Not found in PATH'
    }
    
    all_installed = tools_status['hcxpcapngtool']['installed'] and tools_status['hashcat']['installed']
    
    return jsonify({
        'all_installed': all_installed,
        'tools': tools_status,
        'message': 'All tools installed' if all_installed else 'Some tools are missing. See docs/INSTALL_TOOLS.md for installation instructions.'
    })

if __name__ == '__main__':
    # Determine host binding based on security settings
    if RESTRICT_TO_LOCALHOST:
        host = '127.0.0.1'
        access_msg = "Access from this computer only:"
        access_urls = ["  * http://localhost:5000"]
    else:
        import socket
        hostname = socket.gethostname()
        try:
            local_ip = socket.gethostbyname(hostname)
        except:
            local_ip = "localhost"
        host = '0.0.0.0'
        access_msg = "Access from any device on your network:"
        access_urls = [
            f"  * http://localhost:5000",
            f"  * http://{local_ip}:5000"
        ]
    
    # Helper function to safely print (handles Windows console encoding)
    def safe_print(text):
        try:
            print(text)
        except UnicodeEncodeError:
            # Fallback for Windows console that doesn't support emoji
            print(text.encode('ascii', 'ignore').decode('ascii'))
    
    print("\n" + "="*60)
    print("WiFi Cracker Web App")
    print("="*60)
    
    # Security status (using ASCII-safe characters)
    print("\n[SECURITY STATUS]")
    if AUTH_PASSWORD:
        print("  [OK] Authentication: ENABLED (password required)")
    else:
        print("  [WARN] Authentication: DISABLED (set WIFI_CRACKER_PASSWORD to enable)")
    
    if RESTRICT_TO_LOCALHOST:
        print("  [OK] Network Access: RESTRICTED to localhost only")
    else:
        print("  [WARN] Network Access: OPEN to all devices on network")
        print("    (Set WIFI_CRACKER_HOST=127.0.0.1 to restrict)")
    
    print(f"\n{access_msg}")
    for url in access_urls:
        print(url)
    
    if AUTH_PASSWORD:
        print("\n[INFO] Login: Use any username and the password you set")
    
    print("\nPress CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(host=host, port=5000, debug=False)

