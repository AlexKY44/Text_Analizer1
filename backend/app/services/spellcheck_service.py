import language_tool_python


class SpellCheckService:
    def __init__(self):
        self._tools = {}

    def _get_tool(self, lang: str):
        lang_code = 'uk-UA' if lang == 'uk' else 'en-US'
        if lang_code not in self._tools:
            self._tools[lang_code] = language_tool_python.LanguageTool(lang_code)
        return self._tools[lang_code]

    def correct_text_with_stats(self, text: str, language: str = "uk") -> tuple[str, int]:
        tool = self._get_tool(language)

        matches = tool.check(text)
        error_count = len(matches)

        corrected_text = tool.correct(text)

        return corrected_text, error_count


spell_service = SpellCheckService()