from PIL import Image
import imagehash

def detect_duplicate_pages(images: list) -> bool:
    seen = set()
    for img in images:
        hash_val = imagehash.average_hash(img)
        if hash_val in seen:
            return True
        seen.add(hash_val)
    return False