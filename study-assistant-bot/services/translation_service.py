"""
Translation Service
Translate text to different languages
"""

from typing import Optional, Dict, List
from services.ai_service import AIService
from config import Config
from utils.logger import logger


class TranslationService:
    """Service for translating content"""

    def __init__(self):
        """Initialize translation service"""
        self.ai_service = AIService()
        self.supported_languages = Config.SUPPORTED_LANGUAGES

    def translate(self, text: str, target_language: str, source_language: str = "English") -> Optional[str]:
        """
        Translate text from source to target language

        Args:
            text: Text to translate
            target_language: Target language name
            source_language: Source language name

        Returns:
            Translated text or None
        """
        try:
            if target_language not in self.supported_languages.values():
                logger.error(f"Unsupported target language: {target_language}")
                return None

            prompt = f"""Translate the following text from {source_language} to {target_language}.
Maintain the original meaning and style. Provide only the translation without explanation.

Original text:
{text}

Translation:"""

            system_prompt = f"You are a professional translator. Translate to {target_language} accurately and naturally."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=4000,
            )

        except Exception as e:
            logger.error(f"Error translating to {target_language}: {e}")
            return None

    def translate_by_language_code(self, text: str, target_code: str) -> Optional[str]:
        """
        Translate using language code

        Args:
            text: Text to translate
            target_code: Target language code

        Returns:
            Translated text or None
        """
        try:
            if target_code not in self.supported_languages:
                logger.error(f"Unknown language code: {target_code}")
                return None

            target_language = self.supported_languages[target_code]
            return self.translate(text, target_language)

        except Exception as e:
            logger.error(f"Error translating with code {target_code}: {e}")
            return None

    def translate_to_multiple_languages(
        self,
        text: str,
        target_codes: List[str],
    ) -> Dict[str, Optional[str]]:
        """
        Translate text to multiple languages

        Args:
            text: Text to translate
            target_codes: List of target language codes

        Returns:
            Dictionary mapping language codes to translations
        """
        results = {}

        for code in target_codes:
            if code in self.supported_languages:
                results[code] = self.translate_by_language_code(text, code)
            else:
                logger.warning(f"Skipping unsupported language code: {code}")

        return results

    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language of given text

        Args:
            text: Text to analyze

        Returns:
            Language name or None
        """
        try:
            prompt = f"""Identify the language of the following text. 
Respond with ONLY the language name, nothing else.

Text:
{text}"""

            system_prompt = "You are a language detection expert. Respond with only the language name."

            result = self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.1,
                max_tokens=50,
            )

            return result.strip() if result else None

        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return None

    def transliterate(self, text: str, source_script: str, target_script: str) -> Optional[str]:
        """
        Transliterate text between different writing systems

        Args:
            text: Text to transliterate
            source_script: Source script name (e.g., "Arabic", "Cyrillic")
            target_script: Target script name (e.g., "Latin", "English")

        Returns:
            Transliterated text or None
        """
        try:
            prompt = f"""Transliterate the following text from {source_script} script to {target_script} script.
Maintain pronunciation and meaning as much as possible.

Original text:
{text}

Transliteration:"""

            system_prompt = f"You are an expert in transliteration. Convert {source_script} to {target_script} accurately."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=2000,
            )

        except Exception as e:
            logger.error(f"Error transliterating: {e}")
            return None

    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get list of supported languages

        Returns:
            Dictionary of language codes and names
        """
        return self.supported_languages.copy()

    def get_language_name(self, code: str) -> Optional[str]:
        """
        Get language name from code

        Args:
            code: Language code

        Returns:
            Language name or None
        """
        return self.supported_languages.get(code)

    def get_language_code(self, name: str) -> Optional[str]:
        """
        Get language code from name

        Args:
            name: Language name

        Returns:
            Language code or None
        """
        for code, language_name in self.supported_languages.items():
            if language_name.lower() == name.lower():
                return code
        return None

    def translate_document_section(
        self,
        text: str,
        section_type: str,
        target_language: str,
    ) -> Optional[str]:
        """
        Translate a specific section of document (e.g., heading, paragraph)

        Args:
            text: Section text
            section_type: Type of section (heading, paragraph, list, etc.)
            target_language: Target language

        Returns:
            Translated text or None
        """
        try:
            prompt = f"""Translate the following {section_type} to {target_language}.
Maintain the original formatting and style.

Original:
{text}

Translation:"""

            system_prompt = f"You are a professional translator. Translate to {target_language} maintaining {section_type} format."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=2000,
            )

        except Exception as e:
            logger.error(f"Error translating {section_type}: {e}")
            return None

    def get_translation_status(self) -> Dict:
        """
        Get status of translation service

        Returns:
            Status dictionary
        """
        return {
            "available": True,
            "supported_languages": len(self.supported_languages),
            "languages": self.supported_languages,
        }

    def format_translation_result(self, original: str, translated: str, language: str) -> str:
        """
        Format translation result for display

        Args:
            original: Original text
            translated: Translated text
            language: Target language

        Returns:
            Formatted result
        """
        try:
            result = f"""🌐 Translation to {language}
{'=' * 40}

Original:
{original}

Translation:
{translated}
"""
            return result

        except Exception as e:
            logger.error(f"Error formatting translation: {e}")
            return "Error displaying translation"

    def batch_translate(
        self,
        texts: List[str],
        target_language: str,
    ) -> List[Optional[str]]:
        """
        Translate multiple texts

        Args:
            texts: List of texts to translate
            target_language: Target language

        Returns:
            List of translated texts
        """
        results = []

        for text in texts:
            translated = self.translate(text, target_language)
            results.append(translated)

        return results

    def translate_with_context(
        self,
        text: str,
        target_language: str,
        context: str = "",
    ) -> Optional[str]:
        """
        Translate with context for better accuracy

        Args:
            text: Text to translate
            target_language: Target language
            context: Additional context about the text

        Returns:
            Translated text or None
        """
        try:
            context_part = f"\nContext: {context}" if context else ""

            prompt = f"""Translate the following text to {target_language}.
{context_part}

Original text:
{text}

Translation:"""

            system_prompt = f"You are a professional translator. Translate to {target_language} considering the context."

            return self.ai_service.generate_text(
                prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=2000,
            )

        except Exception as e:
            logger.error(f"Error translating with context: {e}")
            return None
