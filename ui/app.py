
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import time

# Garante que o diretório raiz do projeto está no sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from recorder.ffmpeg_recorder import FFmpegRecorder
from recorder.mux_av import mux

if getattr(sys, 'frozen', False):
    # Executável PyInstaller
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)


class CaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravação de Tela")
        self.output_dir = os.path.abspath(os.path.join(base_dir, '..', 'test'))
        self.recorder = FFmpegRecorder(output_dir=self.output_dir)
        self.is_recording = False

        self.start_btn = tk.Button(root, text="Gravar", command=self.start_recording)
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="Parar", command=self.stop_recording)
        self.stop_btn.pack(pady=10)
        self.stop_btn.config(state=tk.DISABLED)

        self.config_btn = tk.Button(root, text="Configuração", command=self.configurar_pasta)
        self.config_btn.pack(pady=10)

    def configurar_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta de saída")
        if pasta:
            self.output_dir = pasta
            self.recorder.output_dir = pasta
            messagebox.showinfo("Configuração", f"Pasta de saída definida:\n{self.output_dir}")

    def start_recording(self):
        if self.is_recording:
            return
        self.is_recording = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.recorder.start()

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
                    mux(video_path, audio_path, os.path.join(self.output_dir, "saida_muxed.mp4"))

                    # excluir originais
                    try:
                        os.remove(video_path)
                        os.remove(audio_path)
                        print("Arquivos originais removidos.")
                    except Exception as e:
                        print("Erro ao remover arquivos:", e)
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
