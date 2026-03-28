from google.cloud import translate_v2 as translate
from config import get_settings

settings = get_settings()


class TranslationService:
    def __init__(self):
        self.client = translate.Client()

    async def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: str = None
    ) -> str:
        if not text:
            return text

        result = self.client.translate(
            text,
            target_language=target_language,
            source_language=source_language
        )
        return result["translatedText"]

    async def detect_language(self, text: str) -> str:
        if not text:
            return "en"

        result = self.client.detect_language(text)
        return result["language"]

    async def translate_to_english(self, text: str) -> str:
        detected = await self.detect_language(text)
        if detected == "en":
            return text
        return await self.translate_text(text, "en", detected)

    async def translate_to_kinyarwanda(self, text: str) -> str:
        return await self.translate_text(text, "rw")


translation_service = TranslationService()
