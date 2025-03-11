from ultralytics import YOLO

# Загружаем обученную модель
model = YOLO("runs/detect/train/weights/best.pt")

# Применяем на тестовых данных
results = model.predict(source="yolo_dataset/images/test", save=True)

print("✅ Предсказания сохранены в папке runs/detect/predict/")
