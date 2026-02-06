from pydantic import BaseModel
from typing import Optional

class TextRequest(BaseModel):
    text: str
    action: str
    target_language: Optional[str] = "uk"


class TextResponse(BaseModel):
    original_text: str
    processed_text: str
    action: str
    char_count: int
    word_count: int
    error_count: int = 0