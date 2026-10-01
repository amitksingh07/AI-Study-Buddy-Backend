from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import extract_text_from_pdf, extract_text_from_docx

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        return {"success": False, "data": None, "error": {"code": "INVALID_FILE", "message": "Only PDF, DOCX, and TXT files are supported."}}
    
    file_bytes = await file.read()
    if len(file_bytes) > 10 * 1024 * 1024:
        return {"success": False, "data": None, "error": {"code": "FILE_TOO_LARGE", "message": "File exceeds 10MB limit."}}

    try:
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_bytes)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(file_bytes)
        elif file.filename.endswith('.txt'):
            text = file_bytes.decode('utf-8')
            
        if not text.strip():
            return {"success": False, "data": None, "error": {"code": "EMPTY_DOCUMENT", "message": "Could not extract any text."}}
            
        return {"success": True, "data": {"content": text}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "EXTRACTION_ERROR", "message": str(e)}}
