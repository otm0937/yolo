import time
from multiprocessing import Process, Manager

import cv2
from ultralytics import YOLO


def process_frame(original_frames, processed_frames):
    # Load a model
    model = YOLO('yolov8n.pt')

    while True:
        if original_frames.qsize() > 0:
            original_frame = original_frames.get()
            inputs = [original_frame]
            results = model(inputs)
            processed_frames.put(results[0])


def show_frame(processed_frames, captured_time):
    cnt = 0
    avg = 1.0
    max_fps = 0
    min_fps = 100000

    while True:
        if processed_frames.qsize() > 0:
            processd_frame = processed_frames.get()
            processd_plotted = processd_frame.plot()

            prev_time = captured_time.get()

            now_time = time.time()

            dly = now_time - prev_time
            fps = (1 / dly)
            avg = (avg * cnt + fps) / (cnt + 1)
            cnt += 1

            if fps > max_fps:
                max_fps = fps
            if fps < min_fps:
                min_fps = fps

            cv2.putText(processd_plotted, "cnt: %d" % cnt, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
            cv2.putText(processd_plotted, "dly: %.4f" % dly, (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
            cv2.putText(processd_plotted, "fps: %.2f" % fps, (5, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
            cv2.putText(processd_plotted, "avg: %.2f" % avg, (5, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
            cv2.putText(processd_plotted, "max: %.2f" % max_fps, (5, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)
            cv2.putText(processd_plotted, "min: %.2f" % min_fps, (5, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 0), 1)

            cv2.imshow('frame', processd_plotted)

            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break


if __name__ == "__main__":

    cap = cv2.VideoCapture(1)  # set video device #device number
    if cap.isOpened():  # check device connection
        print('width: {}, height : {}'.format(cap.get(3), cap.get(4)))  # print input resolution

    m = Manager()

    original_frames = m.Queue()
    processed_frames = m.Queue()
    captured_time = m.Queue()

    p1 = Process(target=process_frame, args=(original_frames, processed_frames))
    p2 = Process(target=show_frame, args=(processed_frames, captured_time))

    p1.start()
    p2.start()

    while True:  # loop
        ret, frame = cap.read()  # get frame

        if ret:  # check if frame has been grabbed
            frame = cv2.flip(frame, 1)  # flip horizontal
            original_frames.put(frame)
            captured_time.put(time.time())

        else:
            print('error')
            break

    while True:
        if original_frames.qsize() == 0 and processed_frames.qsize() == 0 and captured_time.qsize() == 0:
            p1.terminate()
            p2.terminate()
            break

    cap.release()
    cv2.destroyAllWindows()
