import subprocess
import sys
import os
import webbrowser
import time
import threading
from tkinter import Tk, Label, Button, Text, Scrollbar, Frame
import socket

class WiFiCrackerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Cracker - Launcher")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Try to set window icon (lock icon from shell32.dll)
        try:
            if sys.platform == 'win32':
                import ctypes
                # Set taskbar icon
                myappid = 'wifi.cracker.launcher.1.0'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                # Try to set window icon
                try:
                    icon_path = os.path.join(os.path.dirname(__file__), 'tools', 'icon.ico')
                    if os.path.exists(icon_path):
                        root.iconbitmap(icon_path)
                    else:
                        # Use system lock icon
                        root.iconbitmap(default='@shell32.dll,48')
                except:
                    pass
        except:
            pass
        
        # Configure colors
        bg_color = "#2b2b2b"
        fg_color = "#ffffff"
        button_color = "#667eea"
        
        self.root.configure(bg=bg_color)
        
        # Title
        title = Label(
            root, 
            text="🔓 WiFi Cracker", 
            font=("Arial", 24, "bold"),
            bg=bg_color,
            fg=fg_color
        )
        title.pack(pady=20)
        
        # Status text area
        frame = Frame(root, bg=bg_color)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        
        self.status_text = Text(
            frame,
            height=15,
            width=60,
            bg="#1e1e1e",
            fg="#00ff00",
            font=("Consolas", 10),
            yscrollcommand=scrollbar.set,
            wrap="word"
        )
        self.status_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.status_text.yview)
        
        # Buttons frame
        button_frame = Frame(root, bg=bg_color)
        button_frame.pack(pady=20)
        
        self.start_button = Button(
            button_frame,
            text="🚀 Start Server",
            command=self.start_server,
            bg=button_color,
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = Button(
            button_frame,
            text="⏹ Stop Server",
            command=self.stop_server,
            bg="#dc3545",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        self.open_browser_button = Button(
            button_frame,
            text="🌐 Open Browser",
            command=self.open_browser,
            bg="#28a745",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.open_browser_button.pack(side="left", padx=10)
        
        self.server_process = None
        self.log("Ready to start WiFi Cracker server")
        self.log("Click 'Start Server' to begin")
        self.log("")
        
    def log(self, message):
        self.status_text.insert("end", message + "\n")
        self.status_text.see("end")
        self.root.update()
        
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def check_dependencies(self):
        self.log("Checking Python installation...")
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            self.log(f"✓ Python: {result.stdout.strip()}")
        except:
            self.log("✗ Python not found!")
            return False
        
        self.log("Checking dependencies...")
        try:
            import flask
            self.log("✓ Flask is installed")
            return True
        except ImportError:
            self.log("Installing Flask...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                             check=True, capture_output=True)
                self.log("✓ Dependencies installed successfully")
                return True
            except:
                self.log("✗ Failed to install dependencies")
                return False
    
    def start_server(self):
        if not self.check_dependencies():
            self.log("Cannot start server. Please fix errors above.")
            return
        
        self.log("")
        self.log("=" * 50)
        self.log("Starting WiFi Cracker Server...")
        self.log("=" * 50)
        
        try:
            # Start Flask app
            self.server_process = subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Start reading output in background
            threading.Thread(target=self.read_output, daemon=True).start()
            
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.open_browser_button.config(state="normal")
            
            local_ip = self.get_local_ip()
            self.log("")
            self.log("Server started successfully!")
            self.log("")
            self.log("Access from:")
            self.log(f"  • Your computer: http://localhost:5000")
            self.log(f"  • Your phone: http://{local_ip}:5000")
            self.log("")
            self.log("Waiting for server to be ready...")
            
            # Wait a bit then open browser
            threading.Timer(3.0, self.open_browser).start()
            
        except Exception as e:
            self.log(f"✗ Error starting server: {e}")
    
    def read_output(self):
        if self.server_process:
            for line in iter(self.server_process.stdout.readline, ''):
                if line:
                    self.log(line.strip())
    
    def stop_server(self):
        if self.server_process:
            self.log("Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            self.log("Server stopped")
            
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.open_browser_button.config(state="disabled")
    
    def open_browser(self):
        webbrowser.open("http://localhost:5000")
        self.log("Browser opened!")

if __name__ == "__main__":
    root = Tk()
    app = WiFiCrackerLauncher(root)
    root.mainloop()

