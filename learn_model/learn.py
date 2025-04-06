if __name__ == "__main__":
    from ultralytics import YOLO

    model = YOLO("yolo11n.pt")  # load an official model
    model.train(data="config.yaml", epochs=500, batch=64, optimizer="adam")
    model.export(format="onnx")

    metrics = model.val()  # Запускаем валидацию
    print(f"Точность модели (mAP50-95): {metrics.box.map:.4f}")
    print(f"Точность на IoU=0.5 (mAP50): {metrics.box.map50:.4f}")
    print(f"Точн"
          f"ость на IoU=0.75 (mAP75): {metrics.box.map75:.4f}")