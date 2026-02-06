from pydantic import BaseModel, Field
from typing import Optional

# Базова відповідь
class TextResponse(BaseModel):
    original_text: str
    processed_text: str
    action: str
    char_count: int
    word_count: int
    error_count: int = 0

# 1. Для перекладу
class TranslateRequest(BaseModel):
    text: str
    target_language: str = Field(..., description="Код мови: uk, en, de")

# 2. Для розширення та скорочення (ТУТ Є ВІДСОТКИ)
class ModifyRequest(BaseModel):
    text: str
    language: str = "uk"
    percentage: Optional[int] = Field(None, description="Відсоток зміни")

# 3. [NEW] Для рерайту (ТУТ ВІДСОТКІВ НЕМАЄ)
class RewriteRequest(BaseModel):
    text: str
    language: str = "uk"

# 4. Для перевірки помилок
class SpellCheckRequest(BaseModel):
    text: str
    language: str = "uk"