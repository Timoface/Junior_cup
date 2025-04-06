if __name__ == "__main__":
      from ultralytics import YOLO

      model = YOLO("../runs/detect/train4/weights/best.pt")

      metrics = model.val()  # Запускаем валидацию
      print(f"Точность модели (mAP50-95): {metrics.box.map:.4f}")
      print(f"Точность на IoU=0.5 (mAP50): {metrics.box.map50:.4f}")
      print(f"Точн"
            f"ость на IoU=0.75 (mAP75): {metrics.box.map75:.4f}")
      results = model.predict(source="yolo_dataset/images/test", save=True)

      print("✅ Предсказания сохранены в папке runs/detect/predict/")
