# Extract and Setup Hashcat
$archivePath = "C:\Users\ERA\Downloads\hashcat-7.1.2.7z"
$extractTo = "C:\hashcat"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hashcat Extraction and Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if archive exists
if (-not (Test-Path $archivePath)) {
    Write-Host "[ERROR] Archive not found: $archivePath" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Found archive: $archivePath" -ForegroundColor Green
Write-Host ""

# Check if already extracted
if (Test-Path "$extractTo\hashcat-7.1.2\hashcat.exe") {
    Write-Host "[INFO] Hashcat already extracted at: $extractTo\hashcat-7.1.2" -ForegroundColor Yellow
    $hashcatPath = "$extractTo\hashcat-7.1.2"
} else {
    Write-Host "Extracting hashcat..." -ForegroundColor Cyan
    
    # Create extraction directory
    if (-not (Test-Path $extractTo)) {
        New-Item -ItemType Directory -Path $extractTo -Force | Out-Null
    }
    
    # Extract using 7-Zip
    $7zip = $null
    if (Test-Path "C:\Program Files\7-Zip\7z.exe") {
        $7zip = "C:\Program Files\7-Zip\7z.exe"
    } elseif (Get-Command 7z -ErrorAction SilentlyContinue) {
        $7zip = "7z"
    }
    
    if ($7zip) {
        Write-Host "Using 7-Zip to extract..." -ForegroundColor Cyan
        if ($7zip -eq "7z") {
            & 7z x $archivePath "-o$extractTo" -y | Out-Null
        } else {
            & $7zip x $archivePath "-o$extractTo" -y | Out-Null
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Extraction complete!" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Extraction failed" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "[ERROR] 7-Zip not found. Please extract manually:" -ForegroundColor Red
        Write-Host "  1. Right-click on: $archivePath" -ForegroundColor Yellow
        Write-Host "  2. Select 'Extract to hashcat-7.1.2\'" -ForegroundColor Yellow
        Write-Host "  3. Move the extracted folder to: $extractTo" -ForegroundColor Yellow
        exit 1
    }
    
    $hashcatPath = "$extractTo\hashcat-7.1.2"
}

# Verify hashcat.exe exists
if (-not (Test-Path "$hashcatPath\hashcat.exe")) {
    Write-Host "[ERROR] hashcat.exe not found in: $hashcatPath" -ForegroundColor Red
    Write-Host "Please check the extraction" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[OK] Hashcat found at: $hashcatPath\hashcat.exe" -ForegroundColor Green

# Test hashcat
Write-Host ""
Write-Host "Testing hashcat..." -ForegroundColor Cyan
$version = & "$hashcatPath\hashcat.exe" --version 2>&1 | Select-Object -First 1
Write-Host "[OK] $version" -ForegroundColor Green

# Add to PATH
Write-Host ""
Write-Host "Adding to PATH..." -ForegroundColor Cyan
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

if ($currentPath -like "*$hashcatPath*") {
    Write-Host "[INFO] Already in PATH" -ForegroundColor Yellow
} else {
    $newPath = "$currentPath;$hashcatPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[OK] Added to PATH: $hashcatPath" -ForegroundColor Green
    Write-Host "[INFO] Restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
}

# Test in current session
$env:Path += ";$hashcatPath"
Write-Host ""
Write-Host "Testing in current session..." -ForegroundColor Cyan
& hashcat --version 2>&1 | Select-Object -First 1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Hashcat is ready at: $hashcatPath\hashcat.exe" -ForegroundColor Green
Write-Host ""

