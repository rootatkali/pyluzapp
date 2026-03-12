from datetime import datetime, timedelta
import pytest
from luzapp.models.lesson import Lesson


def make_lesson(**kwargs) -> Lesson:
    defaults = dict(
        lesson_id=12345,
        start_time=datetime(2026, 3, 17, 13, 0, 0),
        wanted_length=timedelta(minutes=15),
        actual_length=timedelta(minutes=15),
    )
    defaults.update(kwargs)
    return Lesson(**defaults)


def test_basic_construction():
    lesson = make_lesson()
    assert lesson.lesson_id == 12345
    assert lesson.is_break is False
    assert lesson.event_type == "Exercise"


def test_end_time():
    lesson = make_lesson(
        start_time=datetime(2026, 3, 17, 13, 0, 0),
        actual_length=timedelta(minutes=45),
    )
    assert lesson.end_time == datetime(2026, 3, 17, 13, 45, 0)


def test_start_timedelta():
    lesson = make_lesson(start_time=datetime(2026, 3, 17, 8, 30, 0))
    assert lesson.start_timedelta == timedelta(hours=8, minutes=30)


def test_end_timedelta():
    lesson = make_lesson(
        start_time=datetime(2026, 3, 17, 8, 30, 0),
        actual_length=timedelta(minutes=45),
    )
    assert lesson.end_timedelta == timedelta(hours=9, minutes=15)


def test_is_lecture_false_by_default():
    lesson = make_lesson(event_type="Exercise")
    assert lesson.is_lecture is False


def test_is_lecture_true():
    lesson = make_lesson(event_type="Lecture")
    assert lesson.is_lecture is True


def test_date_property():
    lesson = make_lesson(start_time=datetime(2026, 3, 17, 13, 0, 0))
    from datetime import date
    assert lesson.date == date(2026, 3, 17)


def test_model_copy_immutability():
    lesson = make_lesson(array="original")
    updated = lesson.model_copy(update={"array": "updated"})
    assert lesson.array == "original"
    assert updated.array == "updated"


def test_frozen_raises_on_mutation():
    lesson = make_lesson()
    with pytest.raises(Exception):
        lesson.array = "mutated"  # type: ignore


def test_default_fields():
    lesson = make_lesson()
    assert lesson.master_id == ""
    assert lesson.bizur == ()
    assert lesson.groups == ()
    assert lesson.tracks == ()
    assert lesson.classes == ()
    assert lesson.background_color == -1
