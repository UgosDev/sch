import numpy as np
from PIL import Image
import cv2

def detect_non_document(image: Image.Image) -> bool:
    img_gray = np.array(image.convert("L"))
    edges = cv2.Canny(img_gray, 50, 150)

    # Documento: tanti bordi rettilinei / pattern regolari
    # Non documento: troppa varietà senza struttura
    edge_density = np.sum(edges > 0) / edges.size
    if edge_density < 0.01:
        return True

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 5:
        return True

    return False