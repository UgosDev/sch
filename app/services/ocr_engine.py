import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from app.services.qr_barcode_reader import read_qr_and_barcodes
from app.services.document_classifier import classify_document
from app.services.field_extractor import extract_fields
from app.services.quality_score import compute_quality_score, interpret_score
from app.services.visual_inspector import analyze_image
from app.services.document_packager import save_text_output
from app.services.non_document_detector import detect_non_document
from app.services.signature_detector import detect_signature
from app.services.page_deduplicator import detect_duplicate_pages
from app.services.text_cleaner import clean_ocr_text
from pathlib import Path
import os

def perform_ocr(filepath: Path):
    if filepath.suffix.lower() == ".pdf":
        images = convert_from_path(str(filepath), dpi=300)
    else:
        images = [Image.open(filepath)]

    raw_text = ""
    barcodes_all_pages = []
    visual_warnings = []
    not_document_flag = False
    signature_found = False

    duplicate_pages = detect_duplicate_pages(images)

    for img in images:
        text = pytesseract.image_to_string(img, lang='ita+eng')
        barcodes = read_qr_and_barcodes(img)
        warnings = analyze_image(img)
        not_a_doc = detect_non_document(img)
        has_signature = detect_signature(img)

        if not_a_doc:
            not_document_flag = True
        if has_signature:
            signature_found = True

        raw_text += text + "\n---\n"
        if barcodes:
            barcodes_all_pages.append(barcodes)
        if warnings:
            visual_warnings.extend(warnings)

    cleaned_text = clean_ocr_text(raw_text)
    doc_type = classify_document(cleaned_text)
    fields = extract_fields(cleaned_text)
    score = compute_quality_score(cleaned_text)
    quality = interpret_score(score)

    session_dir = filepath.parent
    save_text_output(session_dir, filepath.stem, cleaned_text)

    return {
        "text": cleaned_text,
        "barcodes": barcodes_all_pages,
        "doc_type": doc_type,
        "fields": fields,
        "quality_score": score,
        "quality_label": quality,
        "visual_warnings": list(set(visual_warnings)),
        "not_a_document": not_document_flag,
        "signature_detected": signature_found,
        "duplicate_pages_detected": duplicate_pages
    }