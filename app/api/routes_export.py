from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import List
from app.services.export_service import export_anki_csv, export_printable_pdf
from app.schemas.flashcard import Flashcard

router = APIRouter()

class ExportRequest(BaseModel):
    flashcards: List[Flashcard]

@router.post("/anki")
async def export_csv(req: ExportRequest):
    cards = [c.dict() for c in req.flashcards]
    csv_content = export_anki_csv(cards)
    return Response(content=csv_content, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=study_buddy_anki.csv"})

@router.post("/pdf")
async def export_pdf(req: ExportRequest):
    cards = [c.dict() for c in req.flashcards]
    pdf_content = export_printable_pdf(cards)
    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=study_buddy_sheet.pdf"})
