import json
import requests
from fastapi import FastAPI, BackgroundTasks
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

def trigger_comfy_render(data: ReelRequest):
    COMFY_URL = "http://127.0.0.1:8189/prompt"
    with open("/workspace/workflow.json", "r") as f:
        workflow = json.load(f)

    # Mapping Supabase Data to ComfyUI Placeholders
    mapping = {
        "__PROPERTY_NAME__": data.property_name,
        "__PRICE__": data.price,
        "__CTA_TEXT__": data.cta_text,
        "__HUMAN_STYLE_PROMPT__": data.human_style,
        "__OUTPUT_FILENAME__": data.output_filename,
        "__SHOBHA_MODEL_PHOTO__": data.model_photo_url
    }
# Injecting into the Workflow
    for node_id in workflow:
        node = workflow[node_id]
        if isinstance(node, dict) and "inputs" in node:
            for input_key, input_val in node["inputs"].items():
                if isinstance(input_val, str):
                    for placeholder, actual_value in mapping.items():
                        if placeholder in input_val:
                            node["inputs"][input_key] = input_val.replace(placeholder, str(actual_value))

    requests.post(COMFY_URL, json={"prompt": workflow})

@app.post("/generate_reel")
def generate(request: ReelRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(trigger_comfy_render, request)
    return {"status": "queued", "reel_id": request.reel_id}

@app.get("/health")
def health():
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4123)
