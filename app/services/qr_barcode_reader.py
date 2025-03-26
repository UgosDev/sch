from PIL import Image
from pyzbar.pyzbar import decode
from typing import List, Dict

def read_qr_and_barcodes(image: Image.Image) -> List[Dict[str, str]]:
    decoded_objects = decode(image)
    results = []

    for obj in decoded_objects:
        results.append({
            "type": obj.type,
            "data": obj.data.decode("utf-8"),
            "rect": str(obj.rect)
        })

    return results