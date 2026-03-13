import os
import subprocess
from datetime import datetime
import pyautogui
import threading

class FFmpegRecorder:
    def __init__(self, usar_nvenc=False, fps=30, output_dir=None):
        self.usar_nvenc = usar_nvenc
        self.fps = fps
        self.output_dir = output_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test'))
        os.makedirs(self.output_dir, exist_ok=True)
        self.proc = None
        self.thread = None
        self.is_recording = False
        self.output_path = None

    def _build_command(self, largura, altura, saida):
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'gdigrab',
            '-framerate', str(self.fps),
            '-video_size', f'{largura}x{altura}',
            '-i', 'desktop',
        ]
        if self.usar_nvenc:
            comando += ['-c:v', 'h264_nvenc', '-preset', 'fast']
        else:
            comando += ['-c:v', 'libx264', '-preset', 'fast']
        comando += ['-pix_fmt', 'yuv420p', saida]
        return comando

    def start(self):
        if self.is_recording:
            return
        screen_size = pyautogui.size()
        largura, altura = screen_size.width, screen_size.height
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        saida = os.path.abspath(os.path.join(self.output_dir, f'video_{timestamp}.mp4'))
        comando = self._build_command(largura, altura, saida)
        print(' '.join(comando))
        self.proc = subprocess.Popen(comando, stdin=subprocess.PIPE)
        self.is_recording = True
        self.output_path = saida
        self.thread = threading.Thread(target=self._wait)
        self.thread.start()
        return saida

    def _wait(self):
        self.proc.wait()
        self.is_recording = False

    def stop(self):
        if self.is_recording and self.proc:
            try:
                self.proc.stdin.write(b'q')
                self.proc.stdin.flush()
            except Exception:
                self.proc.terminate()
            self.proc.wait()
            self.is_recording = False
            if self.thread:
                self.thread.join()
        return self.output_path
