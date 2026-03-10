import cv2
import sys

# Caminho do vídeo a ser testado
video_path = sys.argv[1] if len(sys.argv) > 1 else "output.mp4"

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Não foi possível abrir o vídeo: {video_path}")
    sys.exit(1)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps if fps > 0 else 0

print(f"FPS: {fps}")
print(f"Frames: {frame_count}")
print(f"Duração (s): {duration}")

cap.release()
