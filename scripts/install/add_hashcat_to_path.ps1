# Add Hashcat to PATH
$hashcatDir = "C:\hashcat\hashcat-7.1.2"

# Verify hashcat exists
if (Test-Path "$hashcatDir\hashcat.exe") {
    Write-Host "[OK] Found hashcat at: $hashcatDir\hashcat.exe" -ForegroundColor Green
    
    # Get current PATH
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    
    # Check if already in PATH
    if ($currentPath -like "*$hashcatDir*") {
        Write-Host "[INFO] Hashcat is already in PATH" -ForegroundColor Yellow
    } else {
        # Add to PATH
        $newPath = "$currentPath;$hashcatDir"
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "[OK] Added hashcat to PATH: $hashcatDir" -ForegroundColor Green
        Write-Host "[INFO] Please restart your terminal/PowerShell for changes to take effect" -ForegroundColor Yellow
    }
    
    # Test in current session
    $env:Path += ";$hashcatDir"
    Write-Host ""
    Write-Host "Testing hashcat in current session..." -ForegroundColor Cyan
    & "$hashcatDir\hashcat.exe" --version 2>&1 | Select-Object -First 1
    
} else {
    Write-Host "[ERROR] hashcat.exe not found at: $hashcatDir\hashcat.exe" -ForegroundColor Red
    Write-Host "Please run setup_hashcat.ps1 first" -ForegroundColor Yellow
}

