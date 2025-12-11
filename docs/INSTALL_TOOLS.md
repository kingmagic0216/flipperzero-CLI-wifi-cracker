# Installing Required Tools on Windows

This guide will help you install `hcxtools` (for `hcxpcapngtool`) and `hashcat` on Windows.

## Quick Installation Guide

### Option 1: Automated Installation Script (Recommended)

Run the installation script:
```powershell
.\scripts\install\install_tools.ps1
```

### Option 2: Manual Installation

Follow the steps below for each tool.

---

## 1. Installing Hashcat

Hashcat is easier to install on Windows.

### Steps:

1. **Download Hashcat:**
   - Visit: https://hashcat.net/hashcat/
   - Click "Download" and select the Windows binary (usually `hashcat-x.x.x.7z`)

2. **Extract Hashcat:**
   - Extract the downloaded `.7z` file to a folder (e.g., `C:\hashcat`)
   - You'll need 7-Zip or WinRAR to extract `.7z` files

3. **Add to PATH (Optional but Recommended):**
   - Open System Properties → Environment Variables
   - Add `C:\hashcat` (or your extraction path) to the PATH variable
   - Or use the script below to add it automatically

4. **Verify Installation:**
   ```cmd
   hashcat --version
   ```

---

## 2. Installing hcxtools (hcxpcapngtool)

hcxtools is primarily a Linux tool, but there are Windows options:

### Option A: Use Pre-built Windows Binary (Easiest)

1. **Download Windows Build:**
   - Visit: https://github.com/ZerBea/hcxtools/releases
   - Look for Windows builds or use WSL

2. **Alternative: Use WSL (Windows Subsystem for Linux)**
   - Install WSL: `wsl --install` in PowerShell (as Administrator)
   - Then install hcxtools in WSL: `sudo apt-get install hcxtools`

### Option B: Build from Source (Advanced)

1. Install MSYS2 or use WSL
2. Follow Linux build instructions

### Option C: Use Alternative Tool

If hcxtools is difficult to install, you can:
- Use WSL (Windows Subsystem for Linux) - recommended
- Use a Linux VM
- Use online conversion tools (less secure)

---

## Automated Installation Script

I'll create a PowerShell script to help automate the installation process.

---

## Verification

After installation, verify both tools are accessible:

```cmd
hashcat --version
hcxpcapngtool -v
```

Or use the web interface: Visit `http://localhost:5000/check/tools` after starting the server.

---

## Troubleshooting

### "Command not found" errors:
- Make sure the tools are in your PATH
- Restart your terminal/command prompt after adding to PATH
- Try using the full path to the executables

### Hashcat GPU issues:
- Install latest GPU drivers (NVIDIA/AMD)
- Hashcat will work on CPU if GPU drivers aren't available

### hcxtools not available:
- Consider using WSL (Windows Subsystem for Linux)
- Or use a Linux VM/container

---

## Quick PATH Setup Script

Run this in PowerShell (as Administrator) to add tools to PATH:

```powershell
# Add hashcat to PATH (adjust path as needed)
$hashcatPath = "C:\hashcat"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$hashcatPath*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$hashcatPath", "User")
    Write-Host "Added hashcat to PATH. Please restart your terminal."
}
```

