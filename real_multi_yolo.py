import time
from multiprocessing import Process, Manager

import cv2
from ultralytics import YOLO


def process_frame(model, frame, processed_frames):
    inputs = [frame]
    result = model(inputs)[0]
    plot = result.plot()

    processed_frames.put(plot)


def show_frame(processed_frames):
    while True:
        if processed_frames.qsize() > 0:
            frame = processed_frames.get()
            cv2.imshow('result', frame)

            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break


if __name__ == "__main__":
    model = YOLO('yolov8n.pt')

    cap = cv2.VideoCapture(1)  # set video device #device number
    if cap.isOpened():  # check device connection
        print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))  # print input resolution

    m = Manager()

    processed_frames = m.Queue()

    Process(target=show_frame, args=(processed_frames,)).start()

    while True:  # loop
        ret, frame = cap.read()  # get frame

        if ret:  # check if frame has been grabbed
            frame = cv2.flip(frame, 1)  # flip horizontal
            print('start: %f' % time.time())
            p = Process(target=process_frame, args=(model, frame, processed_frames))
            p.start()
            print('started: %f' % time.time())
            print('a')


        else:
            print('error')
            break
    cap.release()
    cv2.destroyAllWindows()
