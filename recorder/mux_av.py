import subprocess
import os
from datetime import datetime

def mux(video_path, audio_path, output_dir=None, output_name=None):
    # Se não passar pasta, usa "test" como padrão
    if not output_dir:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test'))

    # garante que a pasta existe
    os.makedirs(output_dir, exist_ok=True)

    # se não passar nome, gera automaticamente com timestamp
    if not output_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"saida_{timestamp}.mp4"

    # monta caminho final corretamente (pasta + nome)
    output_path = os.path.join(output_dir, output_name)

    comando = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',   # converte áudio para AAC
        '-shortest',
        output_path
    ]
    print('MUX CMD:', ' '.join(comando))
    subprocess.run(comando, check=True)
    print(f'Arquivo muxado gerado: {output_path}')

    # remove originais
    try:
        os.remove(video_path)
        os.remove(audio_path)
        print("Arquivos originais removidos.")
    except Exception as e:
        print("Erro ao remover arquivos:", e)

    return output_path


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print('Uso: python mux_av.py <video.mp4> <audio.aac|wav> [saida.mp4]')
        sys.exit(1)
    video = sys.argv[1]
    audio = sys.argv[2]
    saida = sys.argv[3] if len(sys.argv) > 3 else None
    mux(video, audio, output_dir=os.path.dirname(video), output_name=saida)
