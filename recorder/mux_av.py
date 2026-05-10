import subprocess
import sys
import os

def mux(video_path, audio_path, output_path=None):
    # Define a pasta "test" como destino padrão
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test'))

    if not output_path:
        if video_path.lower().endswith('.mp4'):
            output_name = os.path.basename(video_path).replace('.mp4', '_muxed.mp4')
        else:
            output_name = 'output_muxed.mp4'
        output_path = os.path.join(output_dir, output_name)
    else:
        # Se o usuário passar um nome, força salvar dentro da pasta test
        output_path = os.path.join(output_dir, os.path.basename(output_path))

    comando = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'copy',   # se for WAV, reencoda para AAC
        '-shortest',
        output_path
    ]
    print('MUX CMD:', ' '.join(comando))
    subprocess.run(comando, check=True)
    print(f'Arquivo muxado gerado: {output_path}')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Uso: python mux_av.py <video.mp4> <audio.aac|wav> [saida.mp4]')
        sys.exit(1)
    video = sys.argv[1]
    audio = sys.argv[2]
    saida = sys.argv[3] if len(sys.argv) > 3 else None
    mux(video, audio, saida)
