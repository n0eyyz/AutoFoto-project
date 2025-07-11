from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import FileResponse
import uvicorn
import subprocess
import os

app = FastAPI()

MODEL_DIR = "models"
ALLOWED_MODELS = [
    "mobilenetv2.zip",
    "efficientnet_lite.zip",
    "resnet50.zip",
    "clipvision.zip"
]

@app.get("/models")
def models():
    return ("efficientnet_lite.zip", "mobilenetv2.zip", "resnet50.zip", "clipvision.zip")

@app.get("/download-model")
def download_model(model_name: str):
    # # zip 파일이 없거나, 최신화가 필요할 때 zip 생성
    # if not os.path.exists("models/mobilenetv2.zip"):
    #     subprocess.run(["zip", "models/mobilenetv2.zip", "models/mobilenetv2.tflite"])
    if model_name not in ALLOWED_MODELS:
        raise HTTPException(status_code=404, detail="Model not found")

    file_path = os.path.join(MODEL_DIR, model_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File does not exist")

    return FileResponse(file_path, filename=model_name)


if __name__ == "__main__":
    uvicorn.run(
        "server:app",      # 파일명이 server.py일 경우
        host="0.0.0.0",
        port=9000,
        reload=True
    )
