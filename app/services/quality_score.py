import re

def compute_quality_score(text: str) -> float:
    if not text:
        return 0.0

    text_length = len(text)
    word_count = len(re.findall(r'\w+', text))
    symbol_count = len(re.findall(r'[^\w\s]', text))
    line_count = text.count('\n') + 1

    # Penalizza se è troppo corto
    if text_length < 50:
        return 0.2

    # Calcolo euristico semplice
    score = 0.4
    if word_count > 30:
        score += 0.2
    if line_count > 5:
        score += 0.2
    if symbol_count < word_count * 0.1:
        score += 0.2

    return round(min(score, 1.0), 2)

def interpret_score(score: float) -> str:
    if score >= 0.8:
        return "Alta"
    elif score >= 0.5:
        return "Media"
    elif score >= 0.3:
        return "Bassa"
    else:
        return "Molto bassa"