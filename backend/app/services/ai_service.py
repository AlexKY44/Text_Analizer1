import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('models/gemini-flash-latest')

    async def improve_style(self, text: str) -> str:
        prompt = f"Виправ стилістику цього тексту, щоб він звучав професійно та природно. Зберігай мову оригіналу. Поверни лише виправлений текст:\n\n{text}"
        return await self._generate(prompt)

    async def translate(self, text: str, target_lang: str) -> str:
        prompt = f"Переклади на '{target_lang}'. Поверни лише текст:\n\n{text}"
        return await self._generate(prompt)

    async def summarize(self, text: str, percentage: int = None) -> str:
        instruction = f"зменш на {percentage}%" if percentage else "скороти"
        prompt = f"Ти редактор. {instruction}, зберігши мову. Текст:\n\n{text}"
        return await self._generate(prompt)

    async def expand(self, text: str, percentage: int = None) -> str:
        instruction = f"збільш на {percentage}%" if percentage else "розшир"
        prompt = f"Ти редактор. {instruction}, зберігши мову. Текст:\n\n{text}"
        return await self._generate(prompt)

    async def rewrite(self, text: str) -> str:
        prompt = f"Перепиши іншими словами, зберігши мову та стиль. Текст:\n\n{text}"
        return await self._generate(prompt)

    async def _generate(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Помилка AI: {str(e)}"

ai_service = AIService()