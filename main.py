from ultralytics import YOLO
import cv2
import time

# Load a model
model = YOLO('yolov8n.pt')  # load an official detection model
# model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
# model = YOLO('runs/detect/train3/weights/best.pt')  # load a custom model

cap = cv2.VideoCapture(1)
if cap.isOpened():
    print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))

prev_time = time.time()

while True:
    ret, frame = cap.read()

    if ret:
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 360))
        inputs = [frame]
        results = model(inputs)
        res_plotted = results[0].plot()

        now_time = time.time()
        fps = "%.2f" % (1 / (now_time - prev_time))
        prev_time = now_time

        cv2.putText(res_plotted, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow("result", res_plotted)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    else:
        print('error')
        break

cap.release()
cv2.destroyAllWindows()
