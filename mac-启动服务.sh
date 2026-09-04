#!/bin/bash
cd "$(dirname "$0")"
LAN_IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null)"
if [ -z "$LAN_IP" ]; then
  LAN_IP="$(hostname -I 2>/dev/null | awk '{print $1}')"
fi
if [ -z "$LAN_IP" ]; then
  LAN_IP="127.0.0.1"
fi
WORKBENCH_HOST_VALUE="${WORKBENCH_HOST:-127.0.0.1}"
WORKBENCH_PORT_VALUE="${WORKBENCH_PORT:-3000}"
APP_URL="http://127.0.0.1:${WORKBENCH_PORT_VALUE}/"

echo "Starting ComfyUI-API-Modelscope..."
echo "Visit: ${APP_URL}"
if [ "$WORKBENCH_HOST_VALUE" = "0.0.0.0" ] || [ "$WORKBENCH_HOST_VALUE" = "::" ]; then
  echo "LAN: http://${LAN_IP}:${WORKBENCH_PORT_VALUE}/"
  echo "WARNING: LAN mode is unauthenticated; use only on a trusted network."
else
  echo "LAN is disabled by default. Enable explicitly: WORKBENCH_HOST=0.0.0.0 $0"
fi
echo "Press Ctrl+C to stop."
echo ""

# Open browser after 3 seconds
sleep 3 && open "${APP_URL}" &

python3 main.py

echo ""
echo "Server stopped."
