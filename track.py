from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official detection model
model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
model = YOLO('runs/detect/train3/weights/best.pt')  # load a custom model

# Track with the model
results = model.track(source="https://youtu.be/mwHhHh4dXJs", show=True)
results = model.track(source="https://youtu.be/mwHhHh4dXJs", show=True, tracker="bytetrack.yaml")