import tkinter as tk
from recorder.ffmpeg_recorder import FFmpegRecorder
import os
import time
from recorder.mux_av import mux

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
            video_path, audio_path = self.recorder.stop()

            print(f"Vídeo salvo em: {video_path}")
            print(f"Áudio salvo em: {audio_path}")

            # Loop de verificação até que os arquivos existam e tenham tamanho > 0
            for tentativa in range(30):  # tenta até 30 vezes (30s)
                if os.path.exists(video_path) and os.path.getsize(video_path) > 0 \
                   and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                    print("Arquivos válidos encontrados, chamando mux...")
                    mux(video_path, audio_path, "saida.mp4")
                    break
                else:
                    print("Arquivos ainda não prontos, aguardando...")
                    time.sleep(1)
            else:
                print("Erro: arquivos não ficaram prontos dentro do tempo limite.")

            self.is_recording = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureApp(root)
    root.mainloop()
