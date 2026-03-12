from abc import ABC, abstractmethod


class Translator(ABC):
    """Abstract base class for school-specific translation of schedule codes.

    Each school uses opaque internal codes for subject arrays and group names.
    Implement this interface in a school-specific package to map those codes to
    human-readable strings and group email addresses for ICS exports.

    Example::

        class MySchoolTranslator(Translator):
            def translate_subject(self, code: str) -> str:
                return SUBJECTS.get(code, code)

            def translate_group(self, name: str) -> str | None:
                return GROUPS.get(name)
    """

    @abstractmethod
    def translate_subject(self, code: str) -> str:
        """Return a human-readable name for the given subject/array code.

        If the code is unknown, return it unchanged.
        """
        ...

    @abstractmethod
    def translate_group(self, name: str) -> str | None:
        """Return the email address for the given group name, or ``None``.

        The email is used to populate ``ATTENDEE`` lines in ICS exports.
        Return ``None`` if the group should not appear as a calendar attendee.
        """
        ...
