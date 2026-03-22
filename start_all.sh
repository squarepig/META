#!/bin/bash

echo "🚀 Starting DueDoor Reel Factory..."

# 1. Cleanup old processes to free up GPU memory
echo "🧹 Cleaning up old processes..."
pkill -f "python main.py"
pkill -f "python3 /workspace/reel_generator.py"
sleep 2

# 2. Start ComfyUI Engine (Port 8189)
echo "⚙️ Starting ComfyUI Engine..."
cd /workspace/comfyui
nohup python main.py --listen 127.0.0.1 --port 8189 --highvram > /workspace/comfyui.log 2>&1 &
echo $! > /workspace/comfyui.pid

# 3. Wait for Engine to initialize (approx 10 seconds)
sleep 10

# 4. Start Reel Generator API (Port 4123)
echo "🌐 Starting Reel Generator API..."
cd /workspace
nohup python3 /workspace/reel_generator.py > /workspace/reel_generator.log 2>&1 &
echo $! > /workspace/shobha_api.pid

echo "✅ System is UP!"
echo "📡 API: http://127.0.0.1:4123/generate_reel"
echo "📝 Logs: tail -f /workspace/reel_generator.log"
