import os
import subprocess
from datetime import datetime
import pyautogui
import threading

class FFmpegRecorder:
    def __init__(self, usar_nvenc=False, fps=30, output_dir=None,
                 audio_device="audio=Microphone (Intel® Smart Sound Technology (Intel® SST))"):
        self.usar_nvenc = usar_nvenc
        self.fps = fps
        self.output_dir = output_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test'))
        os.makedirs(self.output_dir, exist_ok=True)

        # processos separados
        self.proc_video = None
        self.proc_audio = None
        self.thread_video = None
        self.thread_audio = None

        self.is_recording = False
        self.video_path = None
        self.audio_path = None
        self.audio_device = audio_device

    def _build_video_command(self, largura, altura, saida_video):
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
        comando += ['-pix_fmt', 'yuv420p', saida_video]
        return comando

    def _build_audio_command(self, saida_audio):
        comando = [
            'ffmpeg',
            '-y',
            '-f', 'dshow',
            '-rtbufsize', '100M',
            '-i', self.audio_device,
            '-c:a', 'pcm_s16le',  # WAV sem compressão
            '-ar', '44100',
            '-ac', '2',
            saida_audio
        ]
        return comando

    def start(self):
        if self.is_recording:
            return

        screen_size = pyautogui.size()
        largura, altura = screen_size.width, screen_size.height
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        self.video_path = os.path.abspath(os.path.join(self.output_dir, f'video_{timestamp}.mp4'))
        self.audio_path = os.path.abspath(os.path.join(self.output_dir, f'audio_{timestamp}.wav'))

        comando_video = self._build_video_command(largura, altura, self.video_path)
        comando_audio = self._build_audio_command(self.audio_path)

        print("VIDEO CMD:", ' '.join(comando_video))
        print("AUDIO CMD:", ' '.join(comando_audio))

        # iniciar processos separados
        self.proc_video = subprocess.Popen(comando_video, stdin=subprocess.PIPE)
        self.proc_audio = subprocess.Popen(comando_audio, stdin=subprocess.PIPE)

        self.is_recording = True

        self.thread_video = threading.Thread(target=self._wait_video)
        self.thread_audio = threading.Thread(target=self._wait_audio)
        self.thread_video.start()
        self.thread_audio.start()

        return self.video_path, self.audio_path

    def _wait_video(self):
        self.proc_video.wait()

    def _wait_audio(self):
        self.proc_audio.wait()

    def stop(self):
        if self.is_recording:
            try:
                if self.proc_video:
                    self.proc_video.stdin.write(b'q')
                    self.proc_video.stdin.flush()
                if self.proc_audio:
                    self.proc_audio.stdin.write(b'q')
                    self.proc_audio.stdin.flush()
            except Exception:
                if self.proc_video:
                    self.proc_video.terminate()
                if self.proc_audio:
                    self.proc_audio.terminate()

            if self.proc_video:
                self.proc_video.wait()
            if self.proc_audio:
                self.proc_audio.wait()

            self.is_recording = False

            if self.thread_video:
                self.thread_video.join()
            if self.thread_audio:
                self.thread_audio.join()

        return self.video_path, self.audio_path