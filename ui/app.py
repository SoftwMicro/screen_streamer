import tkinter as tk
from recorder.ffmpeg_recorder import FFmpegRecorder
import os

class CaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravação de Tela")
        self.recorder = FFmpegRecorder()
        self.is_recording = False

        self.start_btn = tk.Button(root, text="Gravar", command=self.start_recording)
        self.start_btn.pack(pady=10)
        self.stop_btn = tk.Button(root, text="Parar", command=self.stop_recording)
        self.stop_btn.pack(pady=10)
        self.stop_btn.config(state=tk.DISABLED)

    def start_recording(self):
        if self.is_recording:
            return
        self.is_recording = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        saida = self.recorder.start()
        self.output_path = saida

    def stop_recording(self):
        if self.is_recording:
            saida = self.recorder.stop()
            print(f'Vídeo salvo em: {saida}')
            video_nome = os.path.basename(saida)
            print(f"Para testar: python test/video_speed_test.py test/{video_nome}")
            self.is_recording = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureApp(root)
    root.mainloop()
