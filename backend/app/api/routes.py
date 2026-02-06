from fastapi import APIRouter
from app.schemas.text import (
    TextResponse, DetailedSpellCheckResponse, SpellCheckResult,
    TranslateRequest, ModifyRequest, SpellCheckRequest, RewriteRequest
)
from app.services.ai_service import ai_service
from app.services.spellcheck_service import spell_service

router = APIRouter()

@router.post("/check", response_model=DetailedSpellCheckResponse)
async def check_grammar(request: SpellCheckRequest):
    # 1. Отримуємо виправлення та список помилок від LanguageTool
    corrected_text, mistakes_list = spell_service.get_detailed_stats(request.text)
    
    # 2. Отримуємо покращений стиль від AI
    style_text = await ai_service.improve_style(request.text)
    
    # 3. Формуємо складну відповідь
    return DetailedSpellCheckResponse(
        original_text=request.text,
        char_count=len(request.text),
        word_count=len(request.text.split()),
        result=SpellCheckResult(
            corrected=corrected_text,
            style_improved=style_text,
            mistakes=mistakes_list
        )
    )

# --- Решта роутів як раніше ---

def _make_response(original: str, processed: str, action: str) -> TextResponse:
    return TextResponse(
        original_text=original,
        processed_text=processed,
        action=action,
        char_count=len(original),
        word_count=len(original.split())
    )

@router.post("/translate", response_model=TextResponse)
async def translate_text(request: TranslateRequest):
    result = await ai_service.translate(request.text, request.target_language)
    return _make_response(request.text, result, "translate")

@router.post("/summarize", response_model=TextResponse)
async def summarize_text(request: ModifyRequest):
    result = await ai_service.summarize(request.text, request.percentage)
    return _make_response(request.text, result, "summarize")

@router.post("/expand", response_model=TextResponse)
async def expand_text(request: ModifyRequest):
    result = await ai_service.expand(request.text, request.percentage)
    return _make_response(request.text, result, "expand")

@router.post("/rewrite", response_model=TextResponse)
async def rewrite_text(request: RewriteRequest):
    result = await ai_service.rewrite(request.text)
    return _make_response(request.text, result, "rewrite")