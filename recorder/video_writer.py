import subprocess

class FFmpegWriter:
    def __init__(self, filename="output.mp4", fps=30, frame_size=(800, 600)):
        self.filename = filename
        self.fps = fps
        self.frame_size = frame_size
        # Comando FFmpeg: recebe frames em raw (BGR) via stdin
        self.process = subprocess.Popen([
            "ffmpeg",
            "-y",
            "-f", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{frame_size[0]}x{frame_size[1]}",
            "-r", str(fps),
            "-i", "-",
            "-vsync", "0",  # Garante FPS constante
            "-c:v", "libx264",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            filename
        ], stdin=subprocess.PIPE)


    def write(self, frame):
        # envia frame bruto para o FFmpeg
        self.process.stdin.write(frame.tobytes())

    def release(self):
        self.process.stdin.close()
        self.process.wait()