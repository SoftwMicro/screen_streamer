import subprocess
import argparse
import time
import sys
import os

def send_signal(rtmp_url):
    """Envia um sinal inicial de 15 segundos (preto + silêncio) para o YouTube."""
    cmd = [
        'ffmpeg',
        '-f', 'lavfi', '-i', 'color=c=black:s=1280x720:r=30',
        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-t', '15',
        '-c:v', 'libx264', '-preset', 'ultrafast', '-b:v', '1000k',
        '-c:a', 'aac', '-b:a', '128k',
        '-f', 'flv', rtmp_url
    ]
    print("[INFO] Enviando sinal inicial de 15 segundos...")
    subprocess.run(cmd)
    print("[INFO] Sinal inicial concluído.")

def run_ffmpeg_rtmp(
    input_file,
    rtmp_url,
    bitrate='6800k',
    preset='ultrafast',
    start_time=None,
    duration=None
):
    """Transmite o vídeo real com faixa de áudio silenciosa."""
    cmd = ['ffmpeg', '-re']

    if start_time is not None:
        cmd += ['-ss', str(start_time)]

    cmd += ['-i', input_file]

    # Áudio silencioso
    cmd += ['-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100']

    if duration is not None:
        cmd += ['-t', str(duration)]

    cmd += [
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-c:v', 'libx264',
        '-preset', preset,
        '-b:v', bitrate,
        '-c:a', 'aac',
        '-b:a', '128k',
        '-shortest',
        '-f', 'flv',
        rtmp_url
    ]

    print("[INFO] Iniciando transmissão do vídeo...")
    print(f"[DEBUG] Comando FFmpeg: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        print(line.strip())
        if 'error' in line.lower() or 'failed' in line.lower():
            print(f"[ERROR-FFMPEG] {line.strip()}")
    proc.wait()

    if proc.returncode == 0:
        print("[INFO] Transmissão finalizada automaticamente ao término do vídeo.")
        return True
    else:
        print(f"[WARN] Falha na transmissão. Código de saída: {proc.returncode}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Transmite um arquivo de vídeo local para YouTube Live com faixa de áudio silenciosa.')
    parser.add_argument('input_file', help='Arquivo de vídeo de entrada (.mp4, .webm, etc)')
    parser.add_argument('--server', choices=['main', 'backup'], default='main', help='Servidor RTMP do YouTube: main (padrão) ou backup')
    parser.add_argument('--key', help='Chave de stream do YouTube (pode ser definida via env YOUTUBE_STREAM_KEY)')
    parser.add_argument('--bitrate', default='6800k', help='Bitrate de vídeo (default: 6800k)')
    parser.add_argument('--preset', default='ultrafast', help='Preset do encoder (default: ultrafast)')
    parser.add_argument('--start', type=float, help='Segundo inicial do vídeo para transmissão (opcional)')
    parser.add_argument('--end', type=float, help='Segundo final do vídeo para transmissão (opcional)')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print(f"[ERROR] Arquivo de entrada não encontrado: {args.input_file}")
        sys.exit(1)

    stream_key = args.key or os.environ.get('YOUTUBE_STREAM_KEY')
    if not stream_key:
        print("[ERROR] Chave de stream não fornecida. Use --key ou defina a variável de ambiente YOUTUBE_STREAM_KEY.")
        sys.exit(1)

    if args.server == 'main':
        rtmp_base = 'rtmp://a.rtmp.youtube.com/live2'
    else:
        rtmp_base = 'rtmp://b.rtmp.youtube.com/live2?backup=1'
    rtmp_url = rtmp_base.rstrip('/') + '/' + stream_key
    print(f"[DEBUG] Usando servidor: {rtmp_base}")
    print(f"[DEBUG] URL RTMP final: {rtmp_url}")

    start_time = args.start if args.start is not None else None
    duration = None
    if args.start is not None and args.end is not None and args.end > args.start:
        duration = args.end - args.start
    elif args.end is not None:
        duration = args.end

    # 1. Enviar sinal inicial
    send_signal(rtmp_url)
    time.sleep(15)

    # 2. Transmitir vídeo real
    run_ffmpeg_rtmp(
        args.input_file,
        rtmp_url,
        args.bitrate,
        args.preset,
        start_time=start_time,
        duration=duration
    )

if __name__ == '__main__':
    main()