from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    success: bool
    data: Optional[dict] = None
    error: Optional[dict] = None
