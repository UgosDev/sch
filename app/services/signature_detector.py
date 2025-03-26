import numpy as np
import cv2
from PIL import Image

def detect_signature(image: Image.Image) -> bool:
    img = np.array(image.convert("L"))
    _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)

    # Trova contorni neri (potenziale firma)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    signature_like = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h) if h > 0 else 0

        # Firma tipica: sottile e lunga
        if 2 < aspect_ratio < 10 and 20 < w < 300 and 10 < h < 100:
            signature_like += 1

    return signature_like > 0