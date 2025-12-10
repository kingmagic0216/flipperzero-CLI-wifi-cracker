# Adding Icons to Launchers

## 🎨 Quick Method (Recommended)

**Double-click:** `Create Shortcuts with Icons.bat`

This will create shortcuts with lock icons on:
- Your Desktop
- The app folder

## 🔧 Manual Method

### Option 1: Create Shortcut Manually

1. Right-click `🚀 START WiFi Cracker (GUI).pyw`
2. Select "Create shortcut"
3. Right-click the shortcut → Properties
4. Click "Change Icon"
5. Browse to: `shell32.dll` (in Windows\System32)
6. Select icon #48 (lock icon) or any other you prefer
7. Click OK

### Option 2: Use Custom Icon File

1. Get/create an `.ico` file
2. Place it in `tools/icon.ico`
3. The GUI launcher will automatically use it

## 📝 Note

- `.pyw` and `.bat` files can't have custom icons directly
- Shortcuts (`.lnk` files) can have icons
- The GUI window will use the icon automatically if available

## 🎯 Icon Suggestions

Good icon choices from `shell32.dll`:
- **#48** - Lock icon (security/encryption theme)
- **#137** - Network/globe icon
- **#138** - WiFi/network icon
- **#19** - Key icon

To browse all icons:
1. Open any shortcut Properties
2. Click "Change Icon"
3. Browse to `shell32.dll`
4. Scroll through available icons

