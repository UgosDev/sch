import cv2
import numpy as np
from PIL import Image

def detect_blur(image: Image.Image) -> bool:
    open_cv_image = np.array(image.convert("L"))
    laplacian_var = cv2.Laplacian(open_cv_image, cv2.CV_64F).var()
    return laplacian_var < 100  # soglia empirica

def detect_low_brightness(image: Image.Image) -> bool:
    gray = np.array(image.convert("L"))
    brightness = np.mean(gray)
    return brightness < 60  # soglia empirica

def detect_blank_page(image: Image.Image) -> bool:
    gray = np.array(image.convert("L"))
    stddev = np.std(gray)
    return stddev < 8  # molto uniforme = probabilmente vuota

def analyze_image(image: Image.Image) -> list:
    warnings = []

    if detect_blur(image):
        warnings.append("Immagine sfocata")

    if detect_low_brightness(image):
        warnings.append("Immagine troppo scura")

    if detect_blank_page(image):
        warnings.append("Pagina apparentemente vuota")

    return warnings