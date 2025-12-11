# WiFi Cracker - Tools Installation Script
# This script helps install hashcat and hcxtools on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WiFi Cracker - Tools Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[WARNING] Not running as Administrator. Some operations may require admin rights." -ForegroundColor Yellow
    Write-Host ""
}

# Function to check if a command exists
function Test-Command {
    param([string]$CommandName)
    $null = Get-Command $CommandName -ErrorAction SilentlyContinue
    return $?
}

# Function to check if a command exists in WSL
function Test-WSLCommand {
    param([string]$CommandName)
    try {
        $result = wsl which $CommandName 2>&1
        return ($result -and $LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

# Function to add to PATH
function Add-ToPath {
    param([string]$PathToAdd)
    
    if (-not (Test-Path $PathToAdd)) {
        Write-Host "[ERROR] Path does not exist: $PathToAdd" -ForegroundColor Red
        return $false
    }
    
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$PathToAdd*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$PathToAdd", "User")
        Write-Host "[OK] Added to PATH: $PathToAdd" -ForegroundColor Green
        return $true
    } else {
        Write-Host "[INFO] Already in PATH: $PathToAdd" -ForegroundColor Yellow
        return $true
    }
}

# Check current status
Write-Host "Checking current installation status..." -ForegroundColor Cyan
Write-Host ""

$hashcatInstalled = Test-Command "hashcat"
$hcxtoolsInstalled = Test-Command "hcxpcapngtool"
$hcxtoolsInWSL = Test-WSLCommand "hcxpcapngtool"

if ($hashcatInstalled) {
    $hashcatVersion = & hashcat --version 2>&1 | Select-Object -First 1
    Write-Host "[OK] Hashcat is installed: $hashcatVersion" -ForegroundColor Green
} else {
    Write-Host "[MISSING] Hashcat is not installed" -ForegroundColor Red
}

if ($hcxtoolsInstalled) {
    $hcxtoolsVersion = & hcxpcapngtool -v 2>&1 | Select-Object -First 1
    Write-Host "[OK] hcxpcapngtool is installed (native): $hcxtoolsVersion" -ForegroundColor Green
} elseif ($hcxtoolsInWSL) {
    $hcxtoolsVersion = wsl hcxpcapngtool -v 2>&1 | Select-Object -First 1
    Write-Host "[OK] hcxpcapngtool is installed (via WSL): $hcxtoolsVersion" -ForegroundColor Green
} else {
    Write-Host "[MISSING] hcxpcapngtool is not installed" -ForegroundColor Red
}

Write-Host ""

# Installation instructions
if (-not $hashcatInstalled -or -not $hcxtoolsInstalled) {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "INSTALLATION INSTRUCTIONS" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    
    if (-not $hashcatInstalled) {
        Write-Host "1. INSTALL HASHCAT:" -ForegroundColor Cyan
        Write-Host "   a) Download from: https://hashcat.net/hashcat/" -ForegroundColor White
        Write-Host "   b) Extract to a folder (e.g., C:\hashcat)" -ForegroundColor White
        Write-Host "   c) Add the folder to your PATH (see below)" -ForegroundColor White
        Write-Host ""
        
        $hashcatPath = Read-Host "   Enter hashcat installation path (or press Enter to skip)"
        if ($hashcatPath -and (Test-Path $hashcatPath)) {
            Add-ToPath $hashcatPath
            Write-Host "   [INFO] Please restart your terminal and run this script again to verify." -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    if (-not $hcxtoolsInstalled) {
        Write-Host "2. INSTALL HCXTOOLS (hcxpcapngtool):" -ForegroundColor Cyan
        Write-Host "   Option A - WSL (Recommended for Windows):" -ForegroundColor White
        Write-Host "     - Install WSL: wsl --install" -ForegroundColor White
        Write-Host "     - Then in WSL: sudo apt-get install hcxtools" -ForegroundColor White
        Write-Host ""
        Write-Host "   Option B - Pre-built Windows binary:" -ForegroundColor White
        Write-Host "     - Check: https://github.com/ZerBea/hcxtools/releases" -ForegroundColor White
        Write-Host "     - Look for Windows builds" -ForegroundColor White
        Write-Host ""
        Write-Host "   Option C - Build from source (Advanced):" -ForegroundColor White
        Write-Host "     - Use MSYS2 or WSL to build" -ForegroundColor White
        Write-Host ""
        
        $hcxtoolsPath = Read-Host "   Enter hcxtools installation path (or press Enter to skip)"
        if ($hcxtoolsPath -and (Test-Path $hcxtoolsPath)) {
            Add-ToPath $hcxtoolsPath
            Write-Host "   [INFO] Please restart your terminal and run this script again to verify." -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "After installation:" -ForegroundColor Yellow
    Write-Host "1. Restart your terminal/command prompt" -ForegroundColor White
    Write-Host "2. Run this script again to verify installation" -ForegroundColor White
    Write-Host "3. Or test manually: hashcat --version" -ForegroundColor White
    Write-Host "========================================" -ForegroundColor Yellow
} else {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "All tools are installed and ready!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
}

Write-Host ""
Write-Host "For detailed instructions, see docs/INSTALL_TOOLS.md" -ForegroundColor Cyan
Write-Host ""

