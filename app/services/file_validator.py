from fastapi import HTTPException
from pathlib import Path
from PIL import Image

MAX_FILE_SIZE_MB = 20
MIN_IMAGE_DIMENSIONS = (800, 600)  # Larghezza x Altezza in pixel

def validate_file_size(path: Path):
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File troppo grande. Limite: 20MB.")

def validate_image_dimensions(path: Path):
    try:
        with Image.open(path) as img:
            width, height = img.size
            if width < MIN_IMAGE_DIMENSIONS[0] or height < MIN_IMAGE_DIMENSIONS[1]:
                raise HTTPException(status_code=400, detail="Immagine troppo piccola per OCR affidabile.")
    except Exception:
        raise HTTPException(status_code=400, detail="Impossibile leggere le dimensioni dell'immagine.")