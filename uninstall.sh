#!/bin/bash
set -e

SERVICE_NAME="livecam"
TARGET_DIR="/opt/livecam"

echo "[+] Stopping service"
sudo systemctl stop $SERVICE_NAME || true
sudo systemctl disable $SERVICE_NAME || true

echo "[+] Removing service file"
sudo rm -f /etc/systemd/system/$SERVICE_NAME.service
sudo systemctl daemon-reload

echo "[+] Removing application files"
sudo rm -rf "$TARGET_DIR"

echo "[✓] Livecam uninstalled"

