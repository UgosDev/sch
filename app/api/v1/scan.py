from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from app.services import ocr_engine, file_validator
from app.utils import temp_manager, logger, api_logger
from app.utils.api_counter import increment_counter
from pathlib import Path
import shutil

router = APIRouter()

@router.post("/scan")
async def scan_document(request: Request, file: UploadFile = File(...)):
    api_key = request.headers.get("X-API-Key")
    
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        logger.log_event("UPLOAD_REJECTED", f"File non supportato: {file.filename}")
        raise HTTPException(status_code=400, detail="Formato file non supportato")

    session_dir = temp_manager.create_temp_dir()
    temp_path = session_dir / file.filename

    try:
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_validator.validate_file_size(temp_path)
        if file.content_type != "application/pdf":
            file_validator.validate_image_dimensions(temp_path)

        logger.log_event("UPLOAD_SUCCESS", f"Ricevuto file: {file.filename}")
        result = ocr_engine.perform_ocr(temp_path)
        logger.log_event("OCR_DONE", f"OCR completato per: {file.filename}")
        api_logger.log_api_usage(api_key=api_key, filename=file.filename)
        request_count = increment_counter(api_key=api_key)
        logger.log_event("API_USAGE", f"{api_key} ha ora effettuato {request_count} richieste oggi.")
    except HTTPException as he:
        logger.log_event("VALIDATION_FAILED", f"{file.filename} - {he.detail}")
        raise he
    except Exception as e:
        logger.log_event("ERROR", f"Errore durante la scansione di {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Errore durante l'elaborazione del documento.")
    finally:
        temp_manager.cleanup_temp_dir(session_dir)

    return {
        "filename": file.filename,
        "text": result["text"],
        "barcodes": result["barcodes"],
        "doc_type": result["doc_type"],
        "fields": result["fields"],
        "quality_score": result["quality_score"],
        "quality_label": result["quality_label"],
        "visual_warnings": result["visual_warnings"]
    }