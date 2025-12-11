# Repository Cleanup Plan

## File Renaming (Remove Emojis)

### Root Level Files:
- `🚀 START WiFi Cracker (GUI).pyw` → `start_wifi_cracker_gui.pyw`
- `🚀 START WiFi Cracker.bat` → `start_wifi_cracker.bat`
- `🎨 Add Icon to Launcher.bat` → `add_icon_to_launcher.bat`
- `🎨 Fix Icon.bat` → `fix_icon.bat`
- `📁 FOLDER STRUCTURE.txt` → `FOLDER_STRUCTURE.txt`

## File Organization

### Installation Scripts → `scripts/install/`
- `install_tools.ps1`
- `install_tools.bat`
- `install_tools_auto.ps1`
- `setup_hashcat.ps1`
- `extract_and_setup_hashcat.ps1`
- `add_hashcat_to_path.ps1`
- `install_wsl_tools.sh`

### Icon Scripts → `tools/icons/`
- `🎨 Add Icon to Launcher.bat` → `add_icon_to_launcher.bat`
- `🎨 Fix Icon.bat` → `fix_icon.bat`
- `tools/Fix Icon.ps1` → `fix_icon.ps1`
- `tools/Create Icon Launcher.bat` → `create_icon_launcher.bat`
- `tools/Create Launcher with Icon.ps1` → `create_launcher_with_icon.ps1`
- `tools/Create Launcher with Icon.vbs` → `create_launcher_with_icon.vbs`
- `tools/Create Shortcuts with Icons.bat` → `create_shortcuts_with_icons.bat`
- `tools/Test Icon.ps1` → `test_icon.ps1`

### Documentation → `docs/`
- Move all `.md` files to `docs/`:
  - `INSTALL_TOOLS.md` → `docs/INSTALL_TOOLS.md`
  - `SECURITY.md` → `docs/SECURITY.md`
  - `TOOLS_SETUP.md` → `docs/TOOLS_SETUP.md`
  - `README_WEB.md` → `docs/README_WEB.md`

### Files to Remove:
- `test_output.txt`
- `IMPLEMENTATION_PLAN_SECURITY.md`
- `PROJECT_AUDIT.md`
- `WALKTHROUGH_SECURITY.md`
- `tests/security_test.py` (if not needed)

## New Structure

```
flipperzero-CLI-wifi-cracker/
├── start_wifi_cracker_gui.pyw      (Main launcher)
├── start_wifi_cracker.bat           (Alternative launcher)
├── app.py
├── requirements.txt
├── LICENSE
├── README.txt
├── .gitignore
│
├── docs/
│   ├── README.txt
│   ├── ICON_SETUP.md
│   ├── INSTALL_TOOLS.md
│   ├── README_WEB.md
│   ├── SECURITY.md
│   ├── TOOLS_SETUP.md
│   └── FOLDER_STRUCTURE.txt
│
├── scripts/
│   ├── install/
│   │   ├── install_tools.ps1
│   │   ├── install_tools.bat
│   │   ├── install_tools_auto.ps1
│   │   ├── setup_hashcat.ps1
│   │   ├── extract_and_setup_hashcat.ps1
│   │   ├── add_hashcat_to_path.ps1
│   │   └── install_wsl_tools.sh
│   ├── bruteforce_attack/
│   └── dictionary_attack
│
├── tools/
│   ├── icons/
│   │   ├── add_icon_to_launcher.bat
│   │   ├── fix_icon.bat
│   │   ├── fix_icon.ps1
│   │   ├── create_icon_launcher.bat
│   │   ├── create_launcher_with_icon.ps1
│   │   ├── create_launcher_with_icon.vbs
│   │   ├── create_shortcuts_with_icons.bat
│   │   └── test_icon.ps1
│   ├── Create Desktop Shortcut.bat
│   ├── clipper.py
│   ├── rpc.py
│   ├── flipperzero_protobuf_py/
│   ├── src/
│   ├── README.md
│   ├── README_ICONS.md
│   └── requirements.txt
│
├── templates/
├── config/
├── temp/          (auto-created)
├── uploads/      (auto-created)
└── wordlists/    (auto-created)
```

