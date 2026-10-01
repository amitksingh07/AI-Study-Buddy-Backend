from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal

class Flashcard(BaseModel):
    id: str
    question: str = Field(..., min_length=5)
    answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=5)
    difficulty: Literal["easy", "medium", "hard"]
    topic: str = Field(..., min_length=2)
    source_page: Optional[int] = None

class FlashcardOutput(BaseModel):
    question: str = Field(..., min_length=5)
    answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=5)
    difficulty: Literal["easy", "medium", "hard"]
    topic: str = Field(..., min_length=2)
    source_page: Optional[int] = None

class FlashcardGenerateRequest(BaseModel):
    content: str
    num_cards: int = 15

class FlashcardGenerateResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[dict] = None
