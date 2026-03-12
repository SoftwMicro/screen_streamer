import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import time
import os
from datetime import datetime
import threading
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
            
            # Gera nome automático para o vídeo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_dir = os.path.join(os.path.dirname(__file__), '..', 'test')
            os.makedirs(test_dir, exist_ok=True)
            filepath = os.path.abspath(os.path.join(test_dir, f'video_{timestamp}.mp4'))

            self.captura = ScreenCapture()
            self.encoder = FrameEncoder(quality=70)

            first_frame = next(self.captura.stream_generator())
            h, w, _ = first_frame.shape
            self.writer = FFmpegWriter(filename=filepath, fps=self.target_fps, frame_size=(w, h))
            print(f"Gravando vídeo em: {filepath}")
            self.is_recording = True
            self.start_time = time.time()  # Marca início
            self.frame_count = 0
            self.record_thread = threading.Thread(target=self.record_loop_thread)
            self.record_thread.start()
  
    def record_loop_thread(self):
        frame_times = []
        while self.is_recording:
            start = time.time()
            frame = next(self.captura.stream_generator())
            encoded_frame = self.encoder.encode(frame)
            decoded = cv2.imdecode(np.frombuffer(encoded_frame, np.uint8), cv2.IMREAD_COLOR)
            self.writer.write(decoded)
            self.frame_count += 1
            elapsed = time.time() - start
            frame_times.append(elapsed)
            print(f"Frame {self.frame_count}: processamento {elapsed:.4f}s")
            sleep_time = max(0, self.frame_interval - elapsed)
            time.sleep(sleep_time)
        # Finaliza gravação
        if self.writer:
            self.writer.release()
        duration = time.time() - self.start_time
        print(f"Tempo real de gravação: {duration:.2f} segundos")
        print(f"Frames gravados: {self.frame_count}")
        if duration > 0:
            real_fps = self.frame_count / duration
            print(f"FPS real: {real_fps:.2f}")
            if real_fps < self.target_fps * 0.95:
                print(f"AVISO: FPS real ({real_fps:.2f}) menor que o desejado ({self.target_fps})! O sistema não conseguiu manter o FPS.")
        if frame_times:
            avg_time = sum(frame_times) / len(frame_times)
            print(f"Tempo médio de processamento por frame: {avg_time:.4f}s")
        print("Gravação finalizada e salva.")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            if hasattr(self, 'record_thread'):
                self.record_thread.join()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureApp(root)
    root.mainloop()