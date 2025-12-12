#!/bin/bash
set -e

TARGET_DIR="/opt/livecam"
SERVICE_NAME="livecam"

REAL_USER=$(logname)

echo "[+] Installing system dependencies"
sudo apt update
sudo apt install -y \
  python3-libcamera \
  python3-kms++ \
  python3-prctl \
  python3-pip \
  python3-venv \
  ffmpeg

echo "[+] Installing application to $TARGET_DIR"
sudo rm -rf "$TARGET_DIR"
sudo cp -r . "$TARGET_DIR"
sudo chown -R "$REAL_USER:$REAL_USER" "$TARGET_DIR"

cd "$TARGET_DIR"

echo "[+] Creating virtual environment with system site packages"
python3 -m venv --system-site-packages .venv
source .venv/bin/activate

echo "[+] Installing Python dependencies"
pip install --upgrade pip
pip install --upgrade numpy
pip install picamera2
pip install -r requirements.txt

echo "[+] Installing systemd service"
sudo cp livecam.service /etc/systemd/system/livecam.service
sudo systemctl daemon-reload
sudo systemctl enable livecam
sudo systemctl restart livecam

echo "[✓] Livecam installed and running"
echo "    http://<PI_IP>:5000"
