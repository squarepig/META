# 1. Clear the broken file and write the fixed version
cat << 'EOF' > /workspace/reel_generator.py
import os
import json
import random
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ReelRequest(BaseModel):
    reel_id: str
    property_name: str
    price: str
    location: str
    audio_script: str
    human_style: str
    cta_text: str
    output_filename: str
    model_photo_url: str
    property_image_url: str

@app.post("/generate_reel")
async def generate_reel(request: ReelRequest):
    workflow = {
        "10": {"class_type": "LoadImageFromURL", "inputs": {"url": request.model_photo_url}},
        "11": {"class_type": "LoadImageFromURL", "inputs": {"url": request.property_image_url}},
        "12": {
            "class_type": "WanVideoGenerator",
            "inputs": {
                "prompt": f"{request.human_style} at {request.property_name}, {request.location}",
                "image": ["10", 0],
                "property_bg": ["11", 0],
                "seed": random.randint(1000, 999999),
                "steps": 25
            }
        },
        "20": {
            "class_type": "SaveVideo", 
            "inputs": {"filename_prefix": request.output_filename, "video": ["12", 0]}
        }
    }
    
    try:
        res = requests.post("http://127.0.0.1:8189/prompt", json={"prompt": workflow})
        if res.status_code != 200:
            return {"status": "error", "comfy_error": res.text}
        return {"status": "queued", "id": request.reel_id, "response": res.json()}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4123)
EOF

# 2. Kill any old stuck processes
pkill -f reel_generator.py

# 3. Start the engine properly
nohup python3 /workspace/reel_generator.py > /workspace/reel_generator.log 2>&1 &

echo "✅ Engine Restarted. Testing connection in 2 seconds..."
sleep 2
curl -s http://127.0.0.1:4123/docs > /dev/null && echo "🚀 PORT 4123 IS NOW LIVE!" || echo "❌ Still not connecting. Check logs."        },
        "20": {
            "class_type": "SaveVideo", 
            "inputs": {"filename_prefix": request.output_filename, "video": ["12", 0]}
        }
    }
    
    try:
        res = requests.post("http://127.0.0.1:8189/prompt", json={"prompt": workflow})
        if res.status_code != 200:
            return {"status": "error", "comfy_error": res.text}
        return {"status": "queued", "id": request.reel_id, "response": res.json()}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4123)
EOF
