from ultralytics import YOLO

def main():
    model = YOLO("yolov8s.pt")

    model.train(
        data="signboard.yaml",
        epochs=50,
        imgsz=640,
        batch=8,
        workers=2,
        device=0,
        project="runs/signboard",
        name="yolov8n_signboard",
        pretrained=True,
        patience=15
    )

if __name__ == "__main__":
    main()