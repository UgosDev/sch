import re

def clean_ocr_text(text: str) -> str:
    # Rimuove righe vuote e simboli casuali inutili
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if len(re.findall(r"[A-Za-z]", line)) < 2 and len(line) < 5:
            continue
        if re.match(r"^[\W_]+$", line):  # solo simboli
            continue
        cleaned.append(line)

    # Rimuove righe duplicate
    seen = set()
    unique_lines = []
    for line in cleaned:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)

    return "\n".join(unique_lines).strip()