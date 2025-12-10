# WiFi Cracker - Web App

A simple, easy-to-use web application for cracking WiFi passwords from PCAP files. Access it from any device on your network - iPhone, Android, laptop, or tablet!

## Features

- 🌐 **Web-based**: Access from any device with a browser
- 📱 **Mobile-friendly**: Responsive design works on phones and tablets
- 🚀 **Easy to use**: Simple drag-and-drop interface
- ⚡ **Quick setup**: Start in seconds

## Prerequisites

Before running the web app, make sure you have:

1. **Python 3.7+** installed
2. **hcxpcapngtool** (from hcxtools package)
   - Linux: `sudo apt-get install hcxtools`
   - macOS: `brew install hcxtools`
   - Windows: Download from [hcxtools releases](https://github.com/ZerBea/hcxtools/releases)
3. **hashcat** installed
   - Linux: `sudo apt-get install hashcat`
   - macOS: `brew install hashcat`
   - Windows: Download from [hashcat website](https://hashcat.net/hashcat/)

## Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the web server:**
   ```bash
   python app.py
   ```

3. **Access from any device:**
   - On your computer: Open browser to `http://localhost:5000`
   - On your phone/tablet: Open browser to `http://YOUR_COMPUTER_IP:5000`
     - Find your IP: 
       - Windows: `ipconfig` (look for IPv4 Address)
       - Mac/Linux: `ifconfig` or `ip addr`

## Usage

1. **Upload PCAP file**: Select the `.pcap`, `.cap`, or `.pcapng` file captured from Flipper Zero
2. **Upload wordlist**: Select your `.txt` wordlist file
3. **Click "Start Cracking"**: The app will process the files and attempt to crack the password
4. **View results**: If the password is found, it will be displayed on screen

## Network Access

To access from other devices on your network:

1. Make sure your computer and phone/tablet are on the same WiFi network
2. Find your computer's local IP address
3. Open `http://YOUR_IP:5000` in your phone's browser

**Note**: Make sure your firewall allows connections on port 5000 if you have issues accessing from other devices.

## Troubleshooting

- **Can't access from phone**: Check firewall settings, ensure both devices are on same network
- **"Command not found" errors**: Make sure `hcxpcapngtool` and `hashcat` are installed and in your PATH
- **Upload fails**: Check file size (max 100MB) and file formats

## Security Note

⚠️ **This tool is for educational purposes only. Only use on networks you own or have explicit permission to test.**

## License

See LICENSE file in the repository.


