from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import subprocess
import os

app = FastAPI()

@app.get("/download-model")
def download_model():
    # # zip 파일이 없거나, 최신화가 필요할 때 zip 생성
    # if not os.path.exists("models/mobilenetv2.zip"):
    #     subprocess.run(["zip", "models/mobilenetv2.zip", "models/mobilenetv2.tflite"])
    return FileResponse("models/mobilenetv2.zip", filename="mobilenetv2.zip")

print("압축파일 전송 완료")

if __name__ == "__main__":
    uvicorn.run(
        "server:app",      # 파일명이 server.py일 경우
        host="0.0.0.0",
        port=9000,
        reload=True
    )
