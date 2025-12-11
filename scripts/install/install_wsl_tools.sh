#!/bin/bash
# Install hcxtools in WSL
# This script can be run from WSL or called via: wsl bash install_wsl_tools.sh

echo "Installing hcxtools in WSL..."
sudo apt-get update
sudo apt-get install -y hcxtools

echo ""
echo "Verifying installation..."
hcxpcapngtool -v

echo ""
echo "Installation complete!"
echo "You can now use: wsl hcxpcapngtool"

