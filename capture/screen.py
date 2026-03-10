import mss
import cv2
import numpy as np

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    def stream_generator(self):
        while True:
            frame = np.array(self.sct.grab(self.monitor))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            yield frame