#!/bin/bash

# =====================================================
# CypherXblade Installer
# Automated environment setup for bug bounty toolkit
# =====================================================

echo -e "\033[92m[+] Updating system packages...\033[0m"
sudo apt update -y

echo -e "\033[92m[+] Installing required system packages...\033[0m"
sudo apt install -y golang git chromium-browser python3-pip

echo -e "\033[92m[+] Installing Python packages...\033[0m"
pip install --upgrade pip
pip install requests beautifulsoup4 pyppeteer

echo -e "\033[92m[+] Installing Pyppeteer Chromium dependencies...\033[0m"
python3 -m pyppeteer install

echo -e "\033[92m[+] Installing ProjectDiscovery tools...\033[0m"
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

echo -e "\033[92m[✓] Installation complete! CypherXblade environment is ready.\033[0m"
echo -e "\033[93m[!] Please ensure that your GOPATH/bin is added to your PATH environment variable to use the installed Go tools.\033[0m"