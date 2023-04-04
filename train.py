from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n.yaml').load('yolov8n.pt')  # build from YAML and transfer weights

# Use the model
results = model.train(
    data='datasets/traffic-coneV2/data.yaml',
    batch=64,
    optimizer='AdamW',
    epochs=100)  # train the model

# results = model.val()  # evaluate model performance on the validation set
# results = model('https://ultralytics.com/images/bus.jpg')  # predict on an image
# success = model.export(format='onnx')  # export the model to ONNX format

#
