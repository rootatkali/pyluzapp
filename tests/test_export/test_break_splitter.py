from datetime import datetime, timedelta
import pytest
from luzapp.models.lesson import Lesson
from luzapp.export.break_splitter import split_lessons_and_breaks


def make_lesson(
    lesson_id: int,
    start_hour: int,
    start_minute: int,
    duration_minutes: int,
    is_break: bool = False,
    day: int = 17,
) -> Lesson:
    return Lesson(
        lesson_id=lesson_id,
        start_time=datetime(2026, 3, day, start_hour, start_minute, 0),
        wanted_length=timedelta(minutes=duration_minutes),
        actual_length=timedelta(minutes=duration_minutes),
        is_break=is_break,
        array="הפסקה" if is_break else "Test",
        display="Break" if is_break else "Lesson",
    )


def test_no_breaks_returns_same():
    lessons = [
        make_lesson(1, 8, 0, 45),
        make_lesson(2, 9, 0, 45),
    ]
    result = split_lessons_and_breaks(lessons)
    # No breaks, lessons should be unchanged
    lesson_ids = {l.lesson_id for l in result if not l.is_break}
    assert 1 in lesson_ids
    assert 2 in lesson_ids


def test_break_outside_lesson_unchanged():
    lesson = make_lesson(1, 8, 0, 45)       # 08:00 - 08:45
    break_ = make_lesson(2, 9, 0, 15, is_break=True)  # 09:00 - 09:15
    result = split_lessons_and_breaks([lesson, break_])
    lessons = [r for r in result if not r.is_break]
    assert len(lessons) == 1
    assert lessons[0].lesson_id == 1
    assert lessons[0].actual_length == timedelta(minutes=45)


def test_break_in_middle_splits_lesson():
    lesson = make_lesson(1, 8, 0, 60)        # 08:00 - 09:00
    break_ = make_lesson(2, 8, 30, 15, is_break=True)  # 08:30 - 08:45
    result = split_lessons_and_breaks([lesson, break_])
    lessons = [r for r in result if not r.is_break]
    assert len(lessons) == 2
    lengths = sorted([l.actual_length for l in lessons])
    assert lengths[0] == timedelta(minutes=15)  # 08:45 - 09:00
    assert lengths[1] == timedelta(minutes=30)  # 08:00 - 08:30


def test_break_at_start_does_not_split():
    # Break starts exactly at lesson start - no overlap
    lesson = make_lesson(1, 8, 30, 60)       # 08:30 - 09:30
    break_ = make_lesson(2, 8, 0, 30, is_break=True)  # 08:00 - 08:30
    result = split_lessons_and_breaks([lesson, break_])
    lessons = [r for r in result if not r.is_break]
    assert len(lessons) == 1


def test_breaks_included_in_output():
    lesson = make_lesson(1, 8, 0, 45)
    break_ = make_lesson(2, 9, 0, 15, is_break=True)
    result = split_lessons_and_breaks([lesson, break_])
    breaks = [r for r in result if r.is_break]
    assert len(breaks) == 1
    assert breaks[0].lesson_id == 2


def test_only_breaks_returns_breaks():
    breaks = [
        make_lesson(1, 8, 0, 15, is_break=True),
        make_lesson(2, 10, 0, 15, is_break=True),
    ]
    result = split_lessons_and_breaks(breaks)
    assert len(result) == 2
    assert all(r.is_break for r in result)


def test_multiple_breaks():
    lesson = make_lesson(1, 8, 0, 120)          # 08:00 - 10:00
    break1 = make_lesson(2, 8, 30, 15, is_break=True)  # 08:30 - 08:45
    break2 = make_lesson(3, 9, 30, 15, is_break=True)  # 09:30 - 09:45
    result = split_lessons_and_breaks([lesson, break1, break2])
    lessons = [r for r in result if not r.is_break]
    assert len(lessons) == 3
