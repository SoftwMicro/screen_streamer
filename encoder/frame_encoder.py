import cv2

class FrameEncoder:
    def __init__(self, quality: int = 80):
        # Qualidade da compressão JPEG (0–100)
        self.quality = quality

    def encode(self, frame):
        # Codifica o frame em JPEG
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
        success, encoded = cv2.imencode('.jpg', frame, encode_param)
        if not success:
            raise ValueError("Erro ao codificar frame")
        return encoded.tobytes()