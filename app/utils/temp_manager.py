import os
import shutil
from pathlib import Path
import uuid

TEMP_DIR = Path("/tmp/scansioni")

def create_temp_dir():
    session_id = str(uuid.uuid4())
    path = TEMP_DIR / session_id
    path.mkdir(parents=True, exist_ok=True)
    return path

def cleanup_temp_dir(path: Path):
    if path.exists() and path.is_dir():
        shutil.rmtree(path)

def split_pdf(pdf_path: Path, output_dir: Path):
    from pdf2image import convert_from_path
    images = convert_from_path(str(pdf_path), dpi=300, output_folder=str(output_dir))
    return images