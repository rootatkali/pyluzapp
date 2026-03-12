from luzapp.translations.base import Translator


class DictTranslator(Translator):
    def __init__(
        self,
        subjects: dict[str, str] | None = None,
        groups: dict[str, str] | None = None,
    ) -> None:
        self._subjects = subjects or {}
        self._groups = groups or {}

    def translate_subject(self, code: str) -> str:
        return self._subjects.get(code, code)

    def translate_group(self, name: str) -> str | None:
        return self._groups.get(name)


class NullTranslator(Translator):
    def translate_subject(self, code: str) -> str:
        return code

    def translate_group(self, name: str) -> str | None:
        return None
