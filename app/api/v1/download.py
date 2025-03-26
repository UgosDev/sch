from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

@router.get("/scan/{session_id}/download")
def download_ocr_output(session_id: str):
    base_path = Path("/tmp/scansioni") / session_id

    if not base_path.exists():
        raise HTTPException(status_code=404, detail="Sessione non trovata")

    output_files = list(base_path.glob("*_output.txt"))
    if not output_files:
        raise HTTPException(status_code=404, detail="Nessun file OCR trovato")

    return FileResponse(output_files[0], media_type="text/plain", filename=output_files[0].name)