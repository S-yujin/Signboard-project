from ultralytics import YOLO

def main():
    model = YOLO(r"C:\Users\win\runs\detect\runs\signboard\yolov8n_signboard5\weights\best.pt")

    model.predict(
        source=r"C:\Users\win\Desktop\signboard-project\dataset\images\test",
        conf=0.25,
        save=True,
        imgsz=640,
        project=r"C:\Users\win\runs\predict",
        name="signboard_test"
    )

if __name__ == "__main__":
    main()