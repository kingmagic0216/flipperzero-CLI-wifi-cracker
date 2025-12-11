# Setup Hashcat from downloaded archive
# This script extracts hashcat and adds it to PATH

$hashcatArchive = "C:\Users\ERA\Downloads\hashcat-7.1.2.7z"
$extractTo = "C:\hashcat"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Hashcat Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if archive exists
if (-not (Test-Path $hashcatArchive)) {
    Write-Host "[ERROR] Hashcat archive not found at: $hashcatArchive" -ForegroundColor Red
    Write-Host "Please download hashcat from: https://hashcat.net/hashcat/" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Found hashcat archive: $hashcatArchive" -ForegroundColor Green
Write-Host ""

# Check for 7-Zip
$7zipPath = $null
if (Test-Path "C:\Program Files\7-Zip\7z.exe") {
    $7zipPath = "C:\Program Files\7-Zip\7z.exe"
} elseif (Get-Command 7z -ErrorAction SilentlyContinue) {
    $7zipPath = "7z"
} else {
    Write-Host "[WARNING] 7-Zip not found. You'll need to extract manually." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Install 7-Zip from https://www.7-zip.org/" -ForegroundColor White
    Write-Host "Option 2: Use WinRAR or another archive tool" -ForegroundColor White
    Write-Host "Option 3: Extract manually and tell me the path" -ForegroundColor White
    Write-Host ""
    
    $manualPath = Read-Host "If already extracted, enter the full path to hashcat folder (or press Enter to skip)"
    if ($manualPath -and (Test-Path $manualPath)) {
        $extractTo = $manualPath
        Write-Host "[OK] Using path: $extractTo" -ForegroundColor Green
    } else {
        Write-Host "[INFO] Please extract the .7z file manually and run this script again" -ForegroundColor Yellow
        exit 0
    }
}

# Extract if 7-Zip is available
if ($7zipPath -and -not (Test-Path $extractTo)) {
    Write-Host "Extracting hashcat to: $extractTo" -ForegroundColor Cyan
    
    # Create extraction directory
    New-Item -ItemType Directory -Path $extractTo -Force | Out-Null
    
    # Extract
    if ($7zipPath -eq "7z") {
        & 7z x $hashcatArchive "-o$extractTo" -y
    } else {
        & $7zipPath x $hashcatArchive "-o$extractTo" -y
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Extraction complete!" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Extraction failed. Please extract manually." -ForegroundColor Red
        exit 1
    }
} elseif (Test-Path $extractTo) {
    Write-Host "[INFO] Directory already exists: $extractTo" -ForegroundColor Yellow
    Write-Host "[INFO] Skipping extraction..." -ForegroundColor Yellow
}

# Find hashcat.exe
$hashcatExe = Get-ChildItem -Path $extractTo -Filter "hashcat.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if (-not $hashcatExe) {
    Write-Host "[WARNING] hashcat.exe not found in $extractTo" -ForegroundColor Yellow
    Write-Host "Please check the extraction and ensure hashcat.exe exists" -ForegroundColor Yellow
    
    # Try to find it
    $possiblePaths = @(
        "$extractTo\hashcat.exe",
        "$extractTo\hashcat-7.1.2\hashcat.exe",
        "$extractTo\hashcat\hashcat.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $hashcatExe = Get-Item $path
            Write-Host "[OK] Found hashcat.exe at: $($hashcatExe.FullName)" -ForegroundColor Green
            break
        }
    }
    
    if (-not $hashcatExe) {
        Write-Host "[ERROR] Could not find hashcat.exe. Please extract manually." -ForegroundColor Red
        exit 1
    }
}

$hashcatDir = $hashcatExe.DirectoryName
Write-Host ""
Write-Host "[OK] Hashcat directory: $hashcatDir" -ForegroundColor Green

# Test hashcat
Write-Host ""
Write-Host "Testing hashcat..." -ForegroundColor Cyan
$version = & "$($hashcatExe.FullName)" --version 2>&1 | Select-Object -First 1
Write-Host "[OK] Hashcat version: $version" -ForegroundColor Green

# Add to PATH
Write-Host ""
$addToPath = Read-Host "Add hashcat to PATH? (y/n)"
if ($addToPath -eq "y") {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$hashcatDir*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$hashcatDir", "User")
        Write-Host "[OK] Added to PATH: $hashcatDir" -ForegroundColor Green
        Write-Host "[INFO] Please restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
    } else {
        Write-Host "[INFO] Already in PATH" -ForegroundColor Yellow
    }
} else {
    Write-Host "[INFO] Not added to PATH. You can use the full path: $($hashcatExe.FullName)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Hashcat is ready to use at: $($hashcatExe.FullName)" -ForegroundColor Green
Write-Host ""

