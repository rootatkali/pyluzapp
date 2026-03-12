from luzapp.translations.base import Translator


class DictTranslator(Translator):
    """Dictionary-backed :class:`Translator` for simple lookup tables.

    Args:
        subjects: Mapping of internal subject/array codes to display names.
            Unknown codes are returned as-is.
        groups: Mapping of group names to email addresses.
            Groups absent from the dict are not added as calendar attendees.

    Example::

        translator = DictTranslator(
            subjects={"MATH": "Mathematics", "ENG": "English"},
            groups={"Alpha": "alpha@school.example.com"},
        )
    """

    def __init__(
        self,
        subjects: dict[str, str] | None = None,
        groups: dict[str, str] | None = None,
    ) -> None:
        self._subjects = subjects or {}
        self._groups = groups or {}

    def translate_subject(self, code: str) -> str:
        """Return the display name for *code*, or *code* itself if unknown."""
        return self._subjects.get(code, code)

    def translate_group(self, name: str) -> str | None:
        """Return the email address for *name*, or ``None`` if not in the dict."""
        return self._groups.get(name)


class NullTranslator(Translator):
    """No-op :class:`Translator` that returns codes unchanged and no group emails.

    Used as the default when no school-specific translator is provided.
    """

    def translate_subject(self, code: str) -> str:
        return code

    def translate_group(self, name: str) -> str | None:
        return None
