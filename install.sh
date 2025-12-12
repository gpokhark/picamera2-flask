#!/bin/bash
set -e

REPO_DIR="$(pwd)"
TARGET_DIR="/opt/livecam"
SERVICE_NAME="livecam.service"

echo "[+] Installing system dependencies"
sudo apt update
sudo apt install -y python3-venv python3-picamera2 libcamera-apps

echo "[+] Installing to $TARGET_DIR"
sudo rm -rf "$TARGET_DIR"
sudo cp -r "$REPO_DIR" "$TARGET_DIR"
REAL_USER=$(logname)
sudo chown -R "$REAL_USER:$REAL_USER" "$TARGET_DIR"

cd "$TARGET_DIR"

echo "[+] Creating virtual environment"
python3 -m venv .venv
. .venv/bin/activate

echo "[+] Installing Python dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Installing systemd service"
sudo cp livecam.service /etc/systemd/system/livecam.service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable livecam
sudo systemctl restart livecam

echo "[✓] Livecam installed and running"
echo "    http://<PI_IP>:5000"

