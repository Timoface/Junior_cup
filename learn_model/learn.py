from ultralytics import YOLO

# Обучаем модель
model = YOLO("yolov8n.pt")  # Можно заменить на yolov8m.pt или yolov8l.pt
model.train(data="config.yaml", epochs=50, imgsz=640, batch=16)
