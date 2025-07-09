from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import ImageResult
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

init_db()

# label에 따라 category 매핑
CATEGORY_MAP = {
    "banana": "음식",
    "apple": "음식",
    "watermelon": "음식",
    "cat": "동물",
    "dog": "동물",
    "mountain": "풍경",
    "valley": "풍경",
    "beach": "풍경",
    # ... 추가 가능
}

def get_category(label: str):
    return CATEGORY_MAP.get(label.lower(), "기타")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flutter 웹 개발 중이므로 모두 허용 (배포 시엔 도메인 제한 추천!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 모델 로딩
model_name = "google/vit-large-patch16-224"
processor = ViTImageProcessor.from_pretrained(model_name)
model = ViTForImageClassification.from_pretrained(model_name)
model.eval()

@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    try:
        # 이미지 읽기
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # 이미지 처리
        inputs = processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        
        # 결과 예측
        logits = outputs.logits
        pred_idx = logits.argmax(-1).item()
        label = model.config.id2label[pred_idx]
        # 응답 전송
        return JSONResponse(content={
            "label": label,
            "class_index": pred_idx
        }
        )

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
