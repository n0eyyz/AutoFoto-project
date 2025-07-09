from tensorflow.keras.applications import MobileNetV2

# ImageNet 사전학습 가중치 포함
model = MobileNetV2(weights='imagenet')
model.save('mobilenetv2.h5')

print('mobilenetv2.h5 저장 완료!')