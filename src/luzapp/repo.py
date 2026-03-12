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
    """High-level interface to a LuzApp schedule repository on disk.

    A repository is a directory that contains a school configuration file and a
    directory of weekly schedule subdirectories.  All path conventions are
    configurable via constructor arguments so that the same library can serve
    schools whose repositories use different layouts.

    Args:
        root_path: Path to the root of the schedule repository.
        config_file: Filename of the school configuration file relative to
            *root_path*.  Defaults to ``"config.school"``.
        weeks_dir: Name of the subdirectory that contains the per-week
            folders, relative to *root_path*.  Defaults to ``"weeks"``.

    Raises:
        FileNotFoundError: If the school configuration file does not exist at
            the expected location.
    """

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
        """School configuration parsed from the config file.

        The result is cached after the first access.
        """
        return parse_school(self._config_file)

    def list_weeks(self) -> list[int]:
        """Return a sorted list of week numbers present in the repository."""
        return list_weeks(self.weeks_path)

    def get_week(self, number: int) -> WeekConfig:
        """Return the :class:`WeekConfig` for the given week number.

        Raises:
            FileNotFoundError: If the week directory or its config file does
                not exist.
        """
        return load_week(self.weeks_path, number)

    def get_lessons(self, week_number: int) -> list[Lesson]:
        """Return all lessons stored in the given week.

        Args:
            week_number: The week number whose lessons should be loaded.

        Returns:
            A list of :class:`Lesson` objects in unspecified order.
        """
        return load_all_lessons(get_week_dir(self.weeks_path, week_number))

    def save_lesson(self, week_number: int, lesson: Lesson) -> Path:
        """Persist a lesson to disk, creating the week directory if needed.

        Args:
            week_number: The week in which to store the lesson.
            lesson: The lesson to save.  Its ``lesson_id`` determines the
                filename; an existing file with the same ID is overwritten.

        Returns:
            The path of the written file.
        """
        return save_lesson(get_week_dir(self.weeks_path, week_number), lesson)

    def delete_lesson(self, week_number: int, lesson_id: int) -> None:
        """Delete a lesson file from disk.

        Args:
            week_number: The week containing the lesson.
            lesson_id: ID of the lesson to delete.

        Raises:
            FileNotFoundError: If no lesson with that ID exists in the week.
        """
        delete_lesson(get_week_dir(self.weeks_path, week_number), lesson_id)

    def create_week(self, week_config: WeekConfig) -> Path:
        """Create the directory structure and config file for a new week.

        Args:
            week_config: Configuration for the new week.

        Returns:
            The path of the newly created week directory.
        """
        return create_week(self.weeks_path, week_config)

    def generate_lesson_id(self) -> int:
        """Generate a random lesson ID suitable for use in a new lesson."""
        return generate_lesson_id()

    def export_ics(
        self,
        week_numbers: list[int],
        translator: Translator | None = None,
        split_breaks: bool = True,
    ) -> str:
        """Export lessons from one or more weeks as an iCalendar string.

        Args:
            week_numbers: Weeks to include in the export.
            translator: Optional :class:`~luzapp.translations.base.Translator`
                used to convert subject codes and group names.  Defaults to
                :class:`~luzapp.translations.dict_translator.NullTranslator`.
            split_breaks: When ``True`` (default), lessons that overlap a
                break slot are split into two events around the break.

        Returns:
            A string in iCalendar (``text/calendar``) format.
        """
        lessons = []
        for wn in week_numbers:
            lessons.extend(self.get_lessons(wn))
        return export_ics(lessons, translator=translator, split_breaks=split_breaks)
