# Setting Up Icons for Launchers

## Quick Fix

**Double-click:** `tools/icons/fix_icon.bat`

This will recreate the shortcut with the lock icon.

## 🔧 Manual Setup (If Icon Doesn't Appear)

### Method 1: Right-Click Properties

1. **Right-click** `WiFi Cracker.lnk` shortcut
2. Select **"Properties"**
3. Click **"Change Icon"** button
4. Click **"Browse"**
5. Navigate to: `C:\Windows\System32\shell32.dll`
6. **Select icon #48** (lock icon) or scroll to find others
7. Click **OK** → **OK**

### Method 2: Create New Shortcut

1. **Right-click** `start_wifi_cracker_gui.pyw`
2. Select **"Create shortcut"**
3. **Rename** it to "WiFi Cracker"
4. **Right-click** the shortcut → **Properties**
5. Click **"Change Icon"**
6. Browse to `shell32.dll` and select an icon

## 🎯 Good Icon Choices

From `shell32.dll`:
- **#48** - 🔒 Lock icon (security theme)
- **#137** - 🌐 Network/globe icon
- **#138** - 📡 WiFi/network icon  
- **#19** - 🔑 Key icon
- **#24** - 🔐 Lock with key
- **#71** - 🖥️ Computer icon

## 💡 Tips

- **Refresh Explorer**: Press `F5` after creating shortcut
- **Icon Cache**: Windows may need a moment to update
- **Custom Icon**: Place `icon.ico` in `tools/` folder for custom icon

## ❓ Troubleshooting

**Icon still not showing?**
1. Make sure you're looking at the `.lnk` file, not `.pyw`
2. Refresh Windows Explorer (F5)
3. Try a different icon number
4. Restart Windows Explorer (task manager → restart explorer.exe)

