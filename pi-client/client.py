import argparse
import imutils
import time
import cv2
import skvideo.io
import skvideo.datasets

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

    # otherwise, we are reading from a video file

    # initialize the first frame in the video stream
    firstFrame = None

    # loop over the frames of the video
    videogen = skvideo.io.vreader(0)

    for frame in videogen:
        frame = imutils.resize(frame, width=500)

        cv2.imwrite('lol.png',frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        for c in cnts:
            if cv2.contourArea(c) > args["min_area"]:
                img = str(base64.b64encode(np.array(cv2.imencode('.jpg', frame)[1]).tostring()))
                if get_detection_score([img]) > 1:
                    post_to_emotion_detection([img])

        firstFrame = frame

        key = cv2.waitKey(1) & 0xFF

            # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # cleanup the cameras and close any open windows