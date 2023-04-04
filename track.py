from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load an official detection model
model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
# model = YOLO('runs/detect/train3/weights/best.pt')  # load a custom model
model = YOLO('runs/detect/train26/weights/best.pt')  # load a custom model

# Track with the model
results = model.track(source="/Users/tk_mini/autory/study/yolo/datasets/airpods_training/images/IMG_1639.jpeg", show=True)
results = model.track(source="/Users/tk_mini/autory/study/yolo/datasets/airpods_training/images/IMG_1639.jpeg", show=True, tracker="bytetrack.yaml")
# results = model.track(source="https://youtu.be/mwHhHh4dXJs", show=True)
# results = model.track(source="https://youtu.be/mwHhHh4dXJs", show=True, tracker="bytetrack.yaml")
