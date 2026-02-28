#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="ea30_sp26.service"
SERVICE_SRC="./${SERVICE_NAME}"
SERVICE_DST="/lib/systemd/system/${SERVICE_NAME}"

echo "[INFO] Installing ${SERVICE_NAME}"

# Must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "[ERROR] Please run with: sudo ./install.sh"
  exit 1
fi

# Check service file exists
if [ ! -f "${SERVICE_SRC}" ]; then
  echo "[ERROR] Cannot find ${SERVICE_SRC}. Run this script from inside EJnPi directory."
  exit 1
fi

echo "[INFO] Copying service file to ${SERVICE_DST}"
cp "${SERVICE_SRC}" "${SERVICE_DST}"

echo "[INFO] Setting permissions (0644)"
chmod 0644 "${SERVICE_DST}"

echo "[INFO] Reloading systemd..."
systemctl daemon-reload

echo "[INFO] Enabling service at boot..."
systemctl enable "${SERVICE_NAME}"

echo "[INFO] Starting service..."
systemctl restart "${SERVICE_NAME}"

echo "[INFO] Done."
systemctl --no-pager --full status "${SERVICE_NAME}" || true