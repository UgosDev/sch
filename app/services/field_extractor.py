import re
from typing import Dict
from dateparser import parse as parse_date

def extract_fields(text: str) -> Dict[str, str]:
    fields = {}

    # Nome (grezza, prende le prime 2 parole con iniziale maiuscola vicine)
    name_match = re.search(r"([A-Z][a-z]+\s[A-Z][a-z]+)", text)
    if name_match:
        fields["nome"] = name_match.group(1)

    # Codice fiscale (italiano)
    cf_match = re.search(r"[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]", text)
    if cf_match:
        fields["codice_fiscale"] = cf_match.group(0)

    # IBAN (Italia, Svizzera, formato internazionale)
    iban_match = re.search(r"[A-Z]{2}[0-9]{2}[A-Z0-9]{11,30}", text)
    if iban_match:
        fields["iban"] = iban_match.group(0)

    # Numero polizza
    polizza_match = re.search(r"(numero\s+)?polizza[:\s]*([A-Z0-9/-]+)", text.lower())
    if polizza_match:
        fields["numero_polizza"] = polizza_match.group(2).upper()

    # Data
    date_match = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if date_match:
        parsed_date = parse_date(date_match.group(1))
        if parsed_date:
            fields["data"] = parsed_date.strftime("%Y-%m-%d")

    return fields