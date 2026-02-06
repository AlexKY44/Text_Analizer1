from fastapi import APIRouter, HTTPException
# Імпортуємо нові схеми
from app.schemas.text import TextResponse, TranslateRequest, ModifyRequest, SpellCheckRequest
from app.services.ai_service import ai_service
from app.services.spellcheck_service import spell_service

router = APIRouter()

# --- ДОПОМІЖНА ФУНКЦІЯ (Щоб не дублювати код статистики) ---
def _make_response(original: str, processed: str, action: str, errors: int = 0) -> TextResponse:
    return TextResponse(
        original_text=original,
        processed_text=processed,
        action=action,
        char_count=len(original),
        word_count=len(original.split()),
        error_count=errors
    )

# --- ЕНДПОІНТИ ---

@router.post("/check", response_model=TextResponse)
async def check_grammar(request: SpellCheckRequest):
    result_text, errors = spell_service.correct_text_with_stats(request.text, request.language)
    return _make_response(request.text, result_text, "check", errors)

@router.post("/translate", response_model=TextResponse)
async def translate_text(request: TranslateRequest):
    result = await ai_service.translate(request.text, request.target_language)
    return _make_response(request.text, result, "translate")

@router.post("/summarize", response_model=TextResponse)
async def summarize_text(request: ModifyRequest):
    result = await ai_service.summarize(request.text, request.language, request.percentage)
    return _make_response(request.text, result, "summarize")

@router.post("/expand", response_model=TextResponse)
async def expand_text(request: ModifyRequest):
    result = await ai_service.expand(request.text, request.language, request.percentage)
    return _make_response(request.text, result, "expand")
@router.post("/rewrite", response_model=TextResponse)
async def rewrite_text(request: ModifyRequest):
    result = await ai_service.rewrite(request.text, request.language)
    return _make_response(request.text, result, "rewrite")