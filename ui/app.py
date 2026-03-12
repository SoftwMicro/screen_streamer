
import tkinter as tk
import os
import threading
import subprocess
from datetime import datetime
import pyautogui

class CaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravação de Tela")
        self.is_recording = False
        self.ffmpeg_thread = None
        self.ffmpeg_proc = None

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
        self.ffmpeg_thread = threading.Thread(target=self.run_ffmpeg_capture)
        self.ffmpeg_thread.start()

    def run_ffmpeg_capture(self):
        FPS = 30
        # Captura a resolução total da tela
        screen_size = pyautogui.size()
        largura, altura = screen_size.width, screen_size.height
        usar_nvenc = False  # Altere para True se quiser testar NVENC

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        test_dir = os.path.join(os.path.dirname(__file__), '..', 'test')
        os.makedirs(test_dir, exist_ok=True)
        saida = os.path.abspath(os.path.join(test_dir, f'video_{timestamp}.mp4'))

        comando = [
            'ffmpeg',
            '-y',
            '-f', 'gdigrab',
            '-framerate', str(FPS),
            '-video_size', f'{largura}x{altura}',
            '-i', 'desktop',
        ]
        if usar_nvenc:
            comando += ['-c:v', 'h264_nvenc', '-preset', 'fast']
        else:
            comando += ['-c:v', 'libx264', '-preset', 'fast']
        comando += ['-pix_fmt', 'yuv420p', saida]

        print(' '.join(comando))
        self.ffmpeg_proc = subprocess.Popen(comando, stdin=subprocess.PIPE)
        self.ffmpeg_proc.wait()
        print(f'Vídeo salvo em: {saida}')
        # Exibe comando para testar o vídeo salvo
        video_nome = os.path.basename(saida)
        print(f"Para testar: python test/video_speed_test.py test/{video_nome}")
        self.is_recording = False
        self.root.after(0, lambda: self.start_btn.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.stop_btn.config(state=tk.DISABLED))

    def stop_recording(self):
        if self.is_recording and self.ffmpeg_proc:
            try:
                self.ffmpeg_proc.stdin.write(b'q')
                self.ffmpeg_proc.stdin.flush()
            except Exception:
                # fallback para terminate se não conseguir enviar 'q'
                self.ffmpeg_proc.terminate()
            self.ffmpeg_proc.wait()
            self.is_recording = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureApp(root)
    root.mainloop()

