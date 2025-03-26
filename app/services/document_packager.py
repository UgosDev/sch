from pathlib import Path

def save_text_output(session_dir: Path, filename: str, text: str) -> Path:
    output_path = session_dir / f"{filename}_output.txt"
    with output_path.open("w", encoding="utf-8") as f:
        f.write(text)
    return output_path