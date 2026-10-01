from fastapi import APIRouter
from app.schemas.flashcard import FlashcardGenerateRequest, FlashcardGenerateResponse
from app.services.ai_service import generate_flashcards

router = APIRouter()

@router.post("/generate", response_model=FlashcardGenerateResponse)
def generate_cards(req: FlashcardGenerateRequest):
    try:
        cards = generate_flashcards(req.content, req.num_cards)
        return {"success": True, "data": {"flashcards": cards}, "error": None}
    except Exception as e:
        return {"success": False, "data": None, "error": {"code": "AI_ERROR", "message": str(e)}}
