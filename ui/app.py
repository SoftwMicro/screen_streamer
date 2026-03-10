import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

from capture.screen import ScreenCapture
from encoder.frame_encoder import FrameEncoder
from recorder.video_writer import VideoWriter

class CaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravação de Tela")
        self.is_recording = False
        self.writer = None      

        self.start_btn = tk.Button(root, text="Gravar", command=self.start_recording)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="Parar", command=self.stop_recording)
        self.stop_btn.pack(pady=10)

    def start_recording(self):
        if not self.is_recording:
            filepath = filedialog.asksaveasfilename(defaultextension=".avi",
                                                    filetypes=[("AVI files", "*.avi")])
            if not filepath:
                return

            self.captura = ScreenCapture()
            self.encoder = FrameEncoder(quality=70)

            first_frame = next(self.captura.stream_generator())
            h, w, _ = first_frame.shape
            self.writer = VideoWriter(filename=filepath, fps=20, frame_size=(w, h))

            self.is_recording = True
            self.root.after(10, self.record_loop)

    def record_loop(self):
        if not self.is_recording:
            if self.writer:
                self.writer.release()
            print("Gravação finalizada e salva.")
            return

        frame = next(self.captura.stream_generator())
        encoded_frame = self.encoder.encode(frame)
        decoded = cv2.imdecode(np.frombuffer(encoded_frame, np.uint8), cv2.IMREAD_COLOR)
        self.writer.write(decoded)

        # agenda próxima captura sem travar a UI
        self.root.after(10, self.record_loop)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureApp(root)
    root.mainloop()