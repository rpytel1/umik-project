import argparse
import time
import cv2
import sys
import base64
import os
import numpy as np
sys.path.append(os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
from utils.utils import get_detection_score, post_to_emotion_detection

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())

    # camera.open()
    time.sleep(0.25)

    firstFrame = None
    cam = cv2.VideoCapture(0)
    counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print(ret)
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        print(gray.shape)
        print(frame.shape)

        if firstFrame is None:
            firstFrame = gray
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        for c in cnts:
            if cv2.contourArea(c) > args["min_area"] and counter % 12 == 0:
                img = base64.b64encode(np.array(cv2.imencode('.jpeg', frame)[1]).tostring()).decode("utf-8")
                print(img)
                if get_detection_score([img])[0] > -1:
                    post_to_emotion_detection([img])
        counter += 1
        firstFrame = gray