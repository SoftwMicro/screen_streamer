import cv2

class VideoWriter:
    def __init__(self, filename="output.avi", fps=20, frame_size=(800, 600)):
        # Codec XVID (funciona bem no Windows)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)

    def write(self, frame):
        self.writer.write(frame)

    def release(self):
        self.writer.release()