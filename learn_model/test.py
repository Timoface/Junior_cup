from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best.pt")

results = model.predict(source="yolo_dataset/images/test", save=True)

print("✅ Предсказания сохранены в папке runs/detect/predict/")
