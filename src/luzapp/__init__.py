"""
luzapp — Python library for reading and writing LuzApp schedule repositories.

A schedule repository is a directory containing a ``config.school`` XML file and
a ``weeks/`` directory of per-week subdirectories.  The primary entry point is
:class:`ScheduleRepo`, which exposes all read/write operations.

Typical usage::

    from luzapp import ScheduleRepo, DictTranslator

    repo = ScheduleRepo("/path/to/school-repo")
    lessons = repo.get_lessons(week_number=1)
    ics = repo.export_ics([1, 2], translator=DictTranslator(subjects={"MATH": "Mathematics"}))
"""

from luzapp.models.color import NamedColor
from luzapp.models.lesson import Lesson
from luzapp.models.school import SchoolConfig, Group, Track, ClassRoom, StaffGroup, Person
from luzapp.models.week import WeekConfig
from luzapp.repo import ScheduleRepo
from luzapp.translations.base import Translator
from luzapp.translations.dict_translator import DictTranslator, NullTranslator
from luzapp.export.ics import export_ics
from luzapp.operations.id_gen import generate_lesson_id
from luzapp import git

__all__ = [
    "NamedColor",
    "Lesson",
    "SchoolConfig",
    "Group",
    "Track",
    "ClassRoom",
    "StaffGroup",
    "Person",
    "WeekConfig",
    "ScheduleRepo",
    "Translator",
    "DictTranslator",
    "NullTranslator",
    "export_ics",
    "generate_lesson_id",
    "git",
]
