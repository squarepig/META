#!/bin/bash

echo "[1/5] Installing missing System Tools (lsof, fuser, netstat)..."
apt-get update && apt-get install -y psmisc lsof net-tools > /dev/null 2>&1

echo "[2/5] Installing Python Dependencies..."
pip install fastapi uvicorn requests pydantic > /dev/null 2>&1

echo "[3/5] Clearing Ports 8000 and 8188..."
# Use our new tools to make sure the ports are bone-dry
fuser -k 8000/tcp 8188/tcp > /dev/null 2>&1
pkill -9 python3 > /dev/null 2>&1
sleep 2

echo "[4/5] Starting DueDoor API (Port 8000)..."
# Start the API in the background and log to workspace
nohup python3 /workspace/reel_generator.py > /workspace/reel_generator.log 2>&1 &

echo "[5/5] Starting ComfyUI Engine (Port 8188)..."
# Start the render engine with lowvram for the 14B model
cd /workspace/comfyui
nohup python3 main.py --listen 0.0.0.0 --port 8188 --lowvram > /workspace/comfyui.log 2>&1 &

echo "=========================================="
echo "   DUEDOOR ENGINE IS LIVE"
echo "   API: http://localhost:8000/health"
echo "   Comfy: http://localhost:8188"
echo "=========================================="
