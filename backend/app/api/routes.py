from fastapi import APIRouter, HTTPException
from app.schemas.text import TextRequest, TextResponse
from app.services.ai_service import ai_service
from app.services.spellcheck_service import spell_service

router = APIRouter()


@router.post("/analyze", response_model=TextResponse)
async def analyze_text(request: TextRequest):
    try:
        chars = len(request.text)
        words = len(request.text.split())
        errors = 0

        if request.action == "check":
            result_text, errors = spell_service.correct_text_with_stats(
                text=request.text,
                language=request.target_language
            )
        else:
            result_text = await ai_service.process_text(
                text=request.text,
                action=request.action,
                language=request.target_language
            )

        return TextResponse(
            original_text=request.text,
            processed_text=result_text,
            action=request.action,
            char_count=chars,
            word_count=words,
            error_count=errors
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))