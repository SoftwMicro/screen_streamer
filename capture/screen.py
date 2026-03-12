import mss
import cv2
import numpy as np

class ScreenCapture:
    def __init__(self):
        pass

    def stream_generator(self):
        sct = mss.mss()
        monitor = sct.monitors[1]
        while True:
            frame = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            yield frame