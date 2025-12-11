# WiFi Cracker - Automated Tools Installation Script
# This script attempts to automatically install hashcat and hcxtools

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WiFi Cracker - Automated Tools Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[WARNING] This script requires Administrator privileges for some operations." -ForegroundColor Yellow
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne "y") {
        exit
    }
}

# Function to check if a command exists
function Test-Command {
    param([string]$CommandName)
    $null = Get-Command $CommandName -ErrorAction SilentlyContinue
    return $?
}

# Check for package managers
$hasChoco = Test-Command "choco"
$hasScoop = Test-Command "scoop"
$hasWSL = Test-Command "wsl"

Write-Host "Detected package managers:" -ForegroundColor Cyan
Write-Host "  Chocolatey: $(if ($hasChoco) { 'Yes' } else { 'No' })" -ForegroundColor $(if ($hasChoco) { 'Green' } else { 'Yellow' })
Write-Host "  Scoop: $(if ($hasScoop) { 'Yes' } else { 'No' })" -ForegroundColor $(if ($hasScoop) { 'Green' } else { 'Yellow' })
Write-Host "  WSL: $(if ($hasWSL) { 'Yes' } else { 'No' })" -ForegroundColor $(if ($hasWSL) { 'Green' } else { 'Yellow' })
Write-Host ""

# Check current status
$hashcatInstalled = Test-Command "hashcat"
$hcxtoolsInstalled = Test-Command "hcxpcapngtool"

if ($hashcatInstalled -and $hcxtoolsInstalled) {
    Write-Host "[SUCCESS] All tools are already installed!" -ForegroundColor Green
    exit 0
}

# Installation options
Write-Host "Installation Options:" -ForegroundColor Cyan
Write-Host ""

# Option 1: Chocolatey
if ($hasChoco) {
    Write-Host "Option 1: Install via Chocolatey" -ForegroundColor Yellow
    Write-Host "  This will install hashcat via Chocolatey package manager" -ForegroundColor White
    $useChoco = Read-Host "  Install hashcat via Chocolatey? (y/n)"
    
    if ($useChoco -eq "y") {
        Write-Host "  Installing hashcat..." -ForegroundColor Cyan
        try {
            choco install hashcat -y
            Write-Host "  [OK] Hashcat installed via Chocolatey" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Failed to install via Chocolatey: $_" -ForegroundColor Red
        }
    }
}

# Option 2: Scoop
if ($hasScoop) {
    Write-Host ""
    Write-Host "Option 2: Install via Scoop" -ForegroundColor Yellow
    Write-Host "  This will install hashcat via Scoop package manager" -ForegroundColor White
    $useScoop = Read-Host "  Install hashcat via Scoop? (y/n)"
    
    if ($useScoop -eq "y") {
        Write-Host "  Installing hashcat..." -ForegroundColor Cyan
        try {
            scoop install hashcat
            Write-Host "  [OK] Hashcat installed via Scoop" -ForegroundColor Green
        } catch {
            Write-Host "  [ERROR] Failed to install via Scoop: $_" -ForegroundColor Red
        }
    }
}

# Option 3: Manual download helper
Write-Host ""
Write-Host "Option 3: Manual Installation Helper" -ForegroundColor Yellow
Write-Host "  I can help you download and set up the tools manually" -ForegroundColor White
$useManual = Read-Host "  Open download pages and guide? (y/n)"

if ($useManual -eq "y") {
    Write-Host ""
    Write-Host "Opening download pages..." -ForegroundColor Cyan
    
    # Open hashcat download page
    Start-Process "https://hashcat.net/hashcat/"
    Write-Host "  [INFO] Opened hashcat download page" -ForegroundColor Green
    
    # Open hcxtools download page
    Start-Process "https://github.com/ZerBea/hcxtools/releases"
    Write-Host "  [INFO] Opened hcxtools releases page" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "After downloading:" -ForegroundColor Yellow
    Write-Host "  1. Extract hashcat to a folder (e.g., C:\hashcat)" -ForegroundColor White
    Write-Host "  2. Extract hcxtools or install via WSL" -ForegroundColor White
    Write-Host "  3. Run this script again to add to PATH" -ForegroundColor White
}

# Option 4: WSL for hcxtools
if ($hasWSL) {
    Write-Host ""
    Write-Host "Option 4: Install hcxtools via WSL" -ForegroundColor Yellow
    Write-Host "  hcxtools is easier to install on Linux/WSL" -ForegroundColor White
    $useWSL = Read-Host "  Install hcxtools in WSL? (y/n)"
    
    if ($useWSL -eq "y") {
        Write-Host "  Installing hcxtools in WSL..." -ForegroundColor Cyan
        try {
            wsl sudo apt-get update
            wsl sudo apt-get install -y hcxtools
            Write-Host "  [OK] hcxtools installed in WSL" -ForegroundColor Green
            Write-Host "  [INFO] You can use: wsl hcxpcapngtool" -ForegroundColor Yellow
        } catch {
            Write-Host "  [ERROR] Failed to install in WSL: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host ""
    Write-Host "Option 4: Install WSL (Recommended for hcxtools)" -ForegroundColor Yellow
    Write-Host "  WSL makes installing hcxtools much easier on Windows" -ForegroundColor White
    $installWSL = Read-Host "  Install WSL? (y/n)"
    
    if ($installWSL -eq "y") {
        Write-Host "  Installing WSL..." -ForegroundColor Cyan
        try {
            wsl --install
            Write-Host "  [OK] WSL installation started. Please restart your computer when prompted." -ForegroundColor Green
            Write-Host "  [INFO] After restart, run: wsl sudo apt-get install hcxtools" -ForegroundColor Yellow
        } catch {
            Write-Host "  [ERROR] Failed to install WSL: $_" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Re-check status
$hashcatInstalled = Test-Command "hashcat"
$hcxtoolsInstalled = Test-Command "hcxpcapngtool"

if ($hashcatInstalled) {
    Write-Host "[OK] Hashcat: Installed" -ForegroundColor Green
} else {
    Write-Host "[MISSING] Hashcat: Not installed" -ForegroundColor Red
    Write-Host "  Download from: https://hashcat.net/hashcat/" -ForegroundColor Yellow
}

if ($hcxtoolsInstalled) {
    Write-Host "[OK] hcxpcapngtool: Installed" -ForegroundColor Green
} else {
    Write-Host "[MISSING] hcxpcapngtool: Not installed" -ForegroundColor Red
    Write-Host "  Recommended: Install WSL and run: sudo apt-get install hcxtools" -ForegroundColor Yellow
    Write-Host "  Or check: https://github.com/ZerBea/hcxtools/releases" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "For detailed instructions, see docs/INSTALL_TOOLS.md" -ForegroundColor Cyan
Write-Host ""

