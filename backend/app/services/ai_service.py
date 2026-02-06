import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('models/gemini-flash-latest')

    async def translate(self, text: str, target_lang: str) -> str:
        prompt = f"Переклади наступний текст на мову з кодом '{target_lang}'. Поверни лише переклад:\n\n{text}"
        return await self._generate(prompt)

    async def summarize(self, text: str, lang: str, percentage: int = None) -> str:
        instruction = f"зменш обсяг тексту на {percentage}%" if percentage else "максимально лаконічно скороти текст"
        prompt = f"Ти редактор. {instruction}, залишивши лише суть. Мова: {lang}. Текст:\n\n{text}"
        return await self._generate(prompt)

    async def expand(self, text: str, lang: str, percentage: int = None) -> str:
        instruction = f"збільш обсяг тексту на {percentage}%" if percentage else "суттєво розшир текст"
        prompt = f"Ти редактор. {instruction}, додавши деталі. Мова: {lang}. Текст:\n\n{text}"
        return await self._generate(prompt)

    async def rewrite(self, text: str, lang: str) -> str:
        prompt = f"Перепиши цей текст іншими словами, зберігаючи зміст та стиль. Мова: {lang}. Текст:\n\n{text}"
        return await self._generate(prompt)

    # Допоміжний приватний метод, щоб не дублювати try/except
    async def _generate(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Помилка AI: {str(e)}"

ai_service = AIService()