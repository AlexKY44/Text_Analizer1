import language_tool_python

class SpellCheckService:
    def __init__(self):
        self._tool = language_tool_python.LanguageTool('uk-UA')

    def get_detailed_stats(self, text: str):
        matches = self._tool.check(text)
        corrected = self._tool.correct(text)
        
        mistakes = []
        for match in matches:
            mistakes.append({
                "message": match.message,
                "suggestions": match.replacements[:5], 
                "offset": match.offset,
                "length": match.error_length
            })
            
        return corrected, mistakes

spell_service = SpellCheckService()