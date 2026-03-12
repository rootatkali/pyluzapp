from abc import ABC, abstractmethod


class Translator(ABC):
    @abstractmethod
    def translate_subject(self, code: str) -> str: ...

    @abstractmethod
    def translate_group(self, name: str) -> str | None: ...
