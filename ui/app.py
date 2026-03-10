import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import time

from capture.screen import ScreenCapture
from encoder.frame_encoder import FrameEncoder
from recorder.video_writer import FFmpegWriter

class CaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravação de Tela")
        self.is_recording = False
        self.writer = None      

        # FPS alvo
        self.target_fps = 30
        self.frame_interval = 1 / self.target_fps
        self.last_time = 0

        # Botão para iniciar gravação
        self.start_btn = tk.Button(root, text="Gravar", command=self.start_recording)
        self.start_btn.pack(pady=10)

        # Botão para parar gravação
        self.stop_btn = tk.Button(root, text="Parar", command=self.stop_recording)
        self.stop_btn.pack(pady=10)

    def start_recording(self):
        if not self.is_recording:
            filepath = filedialog.asksaveasfilename(defaultextension=".mp4",
                                                    filetypes=[("MP4 files", "*.mp4")])
            if not filepath:
                return

            self.captura = ScreenCapture()
            self.encoder = FrameEncoder(quality=70)

            first_frame = next(self.captura.stream_generator())
            h, w, _ = first_frame.shape
            self.writer = FFmpegWriter(filename=filepath, fps=self.target_fps, frame_size=(w, h))

            self.is_recording = True
            self.last_time = time.time()
            self.root.after(1, self.record_loop)

    def record_loop(self):
        if not self.is_recording:
            if self.writer:
                self.writer.release()
            print("Gravação finalizada e salva.")
            return

        now = time.time()
        if now - self.last_time >= self.frame_interval:
            self.last_time = now

            frame = next(self.captura.stream_generator())
            encoded_frame = self.encoder.encode(frame)
            decoded = cv2.imdecode(np.frombuffer(encoded_frame, np.uint8), cv2.IMREAD_COLOR)
            self.writer.write(decoded)

        # agenda próxima chamada respeitando o intervalo de frame
        self.root.after(int(self.frame_interval * 1000), self.record_loop)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureApp(root)
    root.mainloop()