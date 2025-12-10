# Fix WiFi Cracker shortcut icon
$rootDir = Split-Path -Parent $PSScriptRoot
$shortcutPath = Join-Path $rootDir "WiFi Cracker.lnk"
$launcherPath = Join-Path $rootDir "🚀 START WiFi Cracker (GUI).pyw"

Write-Host "Fixing WiFi Cracker shortcut icon..." -ForegroundColor Cyan
Write-Host ""

# Delete old shortcut
if (Test-Path $shortcutPath) {
    Remove-Item $shortcutPath -Force
    Write-Host "Removed old shortcut" -ForegroundColor Yellow
}

# Create new shortcut with explicit icon path
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $launcherPath
$Shortcut.WorkingDirectory = $rootDir
$Shortcut.Description = "Launch WiFi Cracker Web App"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,48"
$Shortcut.Save()

Write-Host "Shortcut created: $shortcutPath" -ForegroundColor Green
Write-Host "Icon: shell32.dll,48 (lock icon)" -ForegroundColor Cyan
Write-Host ""
Write-Host "If icon does not appear:" -ForegroundColor Yellow
Write-Host "  1. Press F5 in Windows Explorer to refresh"
Write-Host "  2. Or right-click shortcut -> Properties -> Change Icon"
Write-Host "  3. Browse to: C:\Windows\System32\shell32.dll"
Write-Host "  4. Select icon #48 (lock) or any other you prefer"
Write-Host ""

# Verify icon was set
$verify = $WshShell.CreateShortcut($shortcutPath)
Write-Host "Current icon location: $($verify.IconLocation)" -ForegroundColor Cyan
