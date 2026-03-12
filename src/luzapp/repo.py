from functools import cached_property
from pathlib import Path

from luzapp.models.lesson import Lesson
from luzapp.models.school import SchoolConfig
from luzapp.models.week import WeekConfig
from luzapp.serializers.school_serializer import parse_school
from luzapp.operations.lesson_ops import load_all_lessons, save_lesson, delete_lesson
from luzapp.operations.week_ops import list_weeks, create_week, load_week, get_week_dir
from luzapp.operations.id_gen import generate_lesson_id
from luzapp.translations.base import Translator
from luzapp.export.ics import export_ics


class ScheduleRepo:
    def __init__(
        self,
        root_path: Path | str,
        config_file: str = "config.school",
        weeks_dir: str = "weeks",
    ) -> None:
        self.root_path = Path(root_path)
        self._config_file = self.root_path / config_file
        self.weeks_path = self.root_path / weeks_dir
        if not self._config_file.exists():
            raise FileNotFoundError(f"No school config found at {self._config_file}")

    @cached_property
    def school_config(self) -> SchoolConfig:
        return parse_school(self._config_file)

    def list_weeks(self) -> list[int]:
        return list_weeks(self.weeks_path)

    def get_week(self, number: int) -> WeekConfig:
        return load_week(self.weeks_path, number)

    def get_lessons(self, week_number: int) -> list[Lesson]:
        return load_all_lessons(get_week_dir(self.weeks_path, week_number))

    def save_lesson(self, week_number: int, lesson: Lesson) -> Path:
        return save_lesson(get_week_dir(self.weeks_path, week_number), lesson)

    def delete_lesson(self, week_number: int, lesson_id: int) -> None:
        delete_lesson(get_week_dir(self.weeks_path, week_number), lesson_id)

    def create_week(self, week_config: WeekConfig) -> Path:
        return create_week(self.weeks_path, week_config)

    def generate_lesson_id(self) -> int:
        return generate_lesson_id()

    def export_ics(
        self,
        week_numbers: list[int],
        translator: Translator | None = None,
        split_breaks: bool = True,
    ) -> str:
        lessons = []
        for wn in week_numbers:
            lessons.extend(self.get_lessons(wn))
        return export_ics(lessons, translator=translator, split_breaks=split_breaks)
