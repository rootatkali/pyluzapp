from datetime import datetime, timedelta
import pytest
from luzapp.models.lesson import Lesson
from luzapp.export.ics import export_ics
from luzapp.translations.dict_translator import DictTranslator, NullTranslator


def make_lesson(lesson_id: int = 1, **kwargs) -> Lesson:
    defaults = dict(
        lesson_id=lesson_id,
        start_time=datetime(2026, 3, 17, 8, 0, 0),
        wanted_length=timedelta(hours=1),
        actual_length=timedelta(hours=1),
        array="Test",
        display="Test Lesson",
        groups=("GroupA",),
    )
    defaults.update(kwargs)
    return Lesson(**defaults)


def test_export_ics_returns_string():
    lessons = [make_lesson()]
    result = export_ics(lessons)
    assert isinstance(result, str)


def test_export_ics_contains_vcalendar():
    lessons = [make_lesson()]
    result = export_ics(lessons)
    assert "BEGIN:VCALENDAR" in result
    assert "END:VCALENDAR" in result


def test_export_ics_contains_vevent():
    lessons = [make_lesson()]
    result = export_ics(lessons)
    assert "BEGIN:VEVENT" in result
    assert "END:VEVENT" in result


def test_export_empty_lessons():
    result = export_ics([])
    assert "BEGIN:VCALENDAR" in result
    assert "BEGIN:VEVENT" not in result


def test_hidden_bizur_excluded():
    lesson = make_lesson(bizur=("Hidden",))
    result = export_ics([lesson], split_breaks=False)
    assert "BEGIN:VEVENT" not in result


def test_non_hidden_bizur_included():
    lesson = make_lesson(bizur=("Alice",))
    result = export_ics([lesson], split_breaks=False)
    assert "BEGIN:VEVENT" in result


def test_export_with_null_translator():
    lessons = [make_lesson()]
    result = export_ics(lessons, translator=NullTranslator(), split_breaks=False)
    assert "BEGIN:VEVENT" in result


def test_export_with_dict_translator():
    translator = DictTranslator(subjects={"Test": "Translated"})
    lessons = [make_lesson(array="Test")]
    result = export_ics(lessons, translator=translator, split_breaks=False)
    assert "Translated" in result


def test_export_no_split():
    lesson = make_lesson()
    result = export_ics([lesson], split_breaks=False)
    assert "BEGIN:VEVENT" in result
