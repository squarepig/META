cat << 'EOF' > /workspace/reel_generator.py
import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dynamically pick up the port from the environment, default to 8188
COMFY_PORT = os.getenv("COMFY_PORT", "8188")
COMFY_URL = f"http://127.0.0.1:{COMFY_PORT}"

@app.route('/generate_reel', methods=['POST'])
def generate_reel():
    data = request.json
    try:
        # This is where your WanVideo/VGN Workflow JSON lives
        # We send a request to ComfyUI's /prompt endpoint
        print(f"🚀 Sending Job to ComfyUI on {COMFY_URL}...")
        
        # We wrap the user data into the ComfyUI API format
        # Note: You should replace this with your actual VGN workflow JSON if you have it!
        payload = {
            "prompt": {
                "10": { "class_type": "LoadImageFromURL", "inputs": { "url": data.get("model_photo_url") } },
                "11": { "class_type": "LoadImageFromURL", "inputs": { "url": data.get("property_image_url") } }
                # ... the rest of your WanVideo nodes go here
            }
        }
        
        response = requests.post(f"{COMFY_URL}/prompt", json=payload)
        return jsonify({"status": "queued", "comfy_response": response.json()})
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == '__main__':
    print(f"📡 Reel API Bridge starting on Port 4123 (Connecting to Comfy on {COMFY_PORT})...")
    app.run(host='0.0.0.0', port=4123)
EOF
