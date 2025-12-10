# Test different icon options
$WshShell = New-Object -ComObject WScript.Shell
$testPath = "$PSScriptRoot\..\WiFi Cracker Test.lnk"

# Test icon 48 (lock)
$Shortcut = $WshShell.CreateShortcut($testPath)
$Shortcut.TargetPath = "$PSScriptRoot\..\🚀 START WiFi Cracker (GUI).pyw"
$Shortcut.WorkingDirectory = "$PSScriptRoot\.."
$Shortcut.Description = "Test - Lock Icon"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,48"
$Shortcut.Save()

Write-Host "Test shortcut created: WiFi Cracker Test.lnk" -ForegroundColor Green
Write-Host "Icon location: shell32.dll,48 (lock icon)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Other icon options to try:" -ForegroundColor Yellow
Write-Host "  shell32.dll,137 - Network/globe"
Write-Host "  shell32.dll,138 - WiFi/network"  
Write-Host "  shell32.dll,19  - Key"
Write-Host "  shell32.dll,24  - Lock with key"
Write-Host ""
Write-Host "To change icon:" -ForegroundColor Yellow
Write-Host "  1. Right-click shortcut → Properties"
Write-Host "  2. Click 'Change Icon'"
Write-Host "  3. Browse to: C:\Windows\System32\shell32.dll"
Write-Host "  4. Select any icon you like"

