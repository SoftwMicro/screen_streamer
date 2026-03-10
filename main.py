from capture.screen import ScreenCapture
from encoder.frame_encoder import FrameEncoder

def main():
    captura = ScreenCapture()
    encoder = FrameEncoder(quality=70)

    for frame in captura.stream_generator():
        encoded_frame = encoder.encode(frame)
        print(f"Frame comprimido: {len(encoded_frame)} bytes")
        # Aqui futuramente enviaremos via rede

if __name__ == "__main__":
    main()