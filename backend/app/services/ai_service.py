import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class AIService:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.model = genai.GenerativeModel('models/gemini-flash-latest')

    async def process_text(self, text: str, action: str, language: str = "uk") -> str:

        prompt = ""

        if action == "translate":
            prompt = f"Переклади наступний текст на {language} мову. Поверни лише переклад:\n\n{text}"

        elif action == "summarize":
            prompt = f"Скороти цей текст, залишаючи лише головну суть. Мова результату: {language}. Текст:\n\n{text}"

        elif action == "expand":
            prompt = f"Розшир цей текст, додавши деталей та пояснень. Мова результату: {language}. Текст:\n\n{text}"

        elif action == "rewrite":
            prompt = f"Перепиши цей текст іншими словами, зберігаючи зміст. Мова: {language}. Текст:\n\n{text}"

        # elif action == "check":
        #     # На випадок, якщо запит піде сюди помилково, хоча має йти в spellcheck
        #     prompt = f"Виправ граматичні помилки в тексті. Мова: {language}. Текст:\n\n{text}"

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Помилка AI: {str(e)}"


ai_service = AIService()