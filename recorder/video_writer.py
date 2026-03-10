import cv2

class VideoWriter:
    def __init__(self, filename="output.avi", fps=30, frame_size=(800, 600)):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # MJPG funciona bem no Windows
        self.writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)

        if not self.writer.isOpened():
            raise RuntimeError("VideoWriter não inicializou. Verifique codec e caminho.")

    def write(self, frame):
        self.writer.write(frame)

    def release(self):
        self.writer.release()