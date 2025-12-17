#!/bin/bash
echo "[+] Installing CypherXblade dependencies"

sudo apt update
sudo apt install -y golang git chromium-browser

pip install -r requirements.txt
python3 -m pyppeteer install

echo "[+] Install external tools"
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest

echo "[✓] CypherXblade Ready"
