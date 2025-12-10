# Create shortcut with icon for WiFi Cracker
$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootDir = Split-Path -Parent $currentDir
$launcherPath = Join-Path $rootDir "🚀 START WiFi Cracker (GUI).pyw"
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "WiFi Cracker.lnk"
$appShortcutPath = Join-Path $rootDir "WiFi Cracker.lnk"

# Create WScript Shell object
$WScriptShell = New-Object -ComObject WScript.Shell

# Create desktop shortcut
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $launcherPath
$shortcut.WorkingDirectory = $rootDir
$shortcut.Description = "Launch WiFi Cracker Web App"
# Use lock icon from shell32.dll (icon index 48)
$shortcut.IconLocation = "shell32.dll,48"
$shortcut.Save()

# Create app folder shortcut
$appShortcut = $WScriptShell.CreateShortcut($appShortcutPath)
$appShortcut.TargetPath = $launcherPath
$appShortcut.WorkingDirectory = $rootDir
$appShortcut.Description = "Launch WiFi Cracker Web App"
$appShortcut.IconLocation = "shell32.dll,48"
$appShortcut.Save()

Write-Host "✓ Shortcuts created with lock icon!" -ForegroundColor Green
Write-Host "  Desktop: $shortcutPath" -ForegroundColor Cyan
Write-Host "  App folder: $appShortcutPath" -ForegroundColor Cyan

