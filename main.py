import time

import cv2
from ultralytics import YOLO

# Load a model
# model = YOLO('yolov8x.pt')  # load an official detection model
# model = YOLO('yolov8n-seg.pt')  # load an official segmentation model
# model = YOLO('runs/detect/train3/weights/best.pt')  # load a custom model
model = YOLO('runs/detect/train36/weights/best.pt')  # load a custom model

cap = cv2.VideoCapture(1)  # set video device #device number
if cap.isOpened():  # check device connection
    print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))  # print input resolution

prev_time = time.time()  # init time
cnt = 0
avg = 1.0
max_fps = 0
min_fps = 100000

while True:  # loop
    ret, frame = cap.read()  # get frame

    if ret:  # check if frame has been grabbed
        frame = cv2.flip(frame, 1)  # flip horizontal
        # frame = cv2.resize(frame, (640, 360))  # resize frame
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        inputs = [frame]  # make input array
        results = model(inputs)  # detect by model
        res_plotted = results[0].plot()  # plotting model

        # Count Frame
        now_time = time.time()
        dly = now_time - prev_time
        fps = (1 / dly)
        avg = (avg * cnt + fps) / (cnt + 1)
        cnt += 1
        prev_time = now_time

        if fps > max_fps:
            max_fps = fps
        if fps < min_fps:
            min_fps = fps

        cv2.putText(res_plotted, "cnt: %d" % cnt, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
        cv2.putText(res_plotted, "dly: %.4f" % dly, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
        cv2.putText(res_plotted, "fps: %.2f" % fps, (5, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
        cv2.putText(res_plotted, "avg: %.2f" % avg, (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
        cv2.putText(res_plotted, "max: %.2f" % max_fps, (5, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
        cv2.putText(res_plotted, "min: %.2f" % min_fps, (5, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)

        #  Display image
        cv2.imshow("result", res_plotted)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    else:
        print('error')
        break

cap.release()
cv2.destroyAllWindows()
