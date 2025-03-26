def classify_document(text: str) -> str:
    text_lower = text.lower()

    if "disdetta" in text_lower or "recesso" in text_lower:
        return "disdetta"
    elif "polizza" in text_lower or "numero polizza" in text_lower:
        return "polizza"
    elif "offerta" in text_lower or "preventivo" in text_lower:
        return "offerta"
    elif "pagamento" in text_lower or "fattura" in text_lower:
        return "fattura"
    elif "contratto" in text_lower or "stipula" in text_lower:
        return "contratto"
    else:
        return "non classificato"