from datetime import datetime, timedelta
from pathlib import Path
import pytest
from luzapp.serializers.lesson_serializer import parse_lesson, serialize_lesson
from luzapp.models.lesson import Lesson


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
WEEK01_OBJ = FIXTURES_DIR / "weeks" / "week01" / "_obj"


def test_parse_break_lesson(sample_lesson_break):
    lesson = sample_lesson_break
    assert lesson.lesson_id == 1042328123
    assert lesson.array == "הפסקה"
    assert lesson.subject == "הפסקה"
    assert lesson.start_time == datetime(2026, 3, 16, 19, 0, 0)
    assert lesson.wanted_length == timedelta(hours=1, minutes=15)
    assert lesson.actual_length == timedelta(hours=1, minutes=15)
    assert lesson.display == "הפסקת ערב"
    assert lesson.is_break is True
    assert lesson.is_skippable is False
    assert lesson.is_locked is False
    assert lesson.background_color == -1
    assert lesson.event_type == "Exercise"
    assert lesson.groups == ("ונוס",)
    assert lesson.tracks == ("ונוס",)
    assert lesson.classes == ("ונוס",)
    assert lesson.bizur == ()
    assert lesson.master_id == ""
    assert lesson.staff_comment == ""
    assert lesson.task_type == ""
    assert lesson.task_parameters == ""


def test_parse_exercise_lesson(sample_lesson_exercise):
    lesson = sample_lesson_exercise
    assert lesson.lesson_id == 1076807964
    assert lesson.array == "נחש"
    assert lesson.subject == "Conventions"
    assert lesson.start_time == datetime(2026, 3, 17, 13, 0, 0)
    assert lesson.wanted_length == timedelta(minutes=15)
    assert lesson.actual_length == timedelta(minutes=15)
    assert lesson.display == "נחש"
    assert lesson.is_break is False
    assert lesson.background_color == -9728477
    assert lesson.staff_comment == 'ל"ע קונבנציות'
    assert lesson.groups == ("ונוס",)


def test_parse_boolean_false(sample_lesson_break):
    assert sample_lesson_break.is_skippable is False
    assert sample_lesson_break.is_locked is False
    assert sample_lesson_break.is_conversation_potential is False
    assert sample_lesson_break.suppress_room_validation is False


def test_parse_boolean_true():
    xml = """<WeekConfig>
  <LessonInfo lessonId="999">
    <masterId></masterId>
    <lessonArray>test</lessonArray>
    <lessonSubject>test</lessonSubject>
    <lessonStartTime>17/03/2026 13:00:00</lessonStartTime>
    <lessonWantedLength>00:15:00</lessonWantedLength>
    <lessonActualLength>00:15:00</lessonActualLength>
    <lessonDisplay>test</lessonDisplay>
    <lessonIsBreak>True</lessonIsBreak>
    <lessonIsSkippableForRelevantGroups>True</lessonIsSkippableForRelevantGroups>
    <lessonIsLocked>True</lessonIsLocked>
    <lessonIsConversationPotential>True</lessonIsConversationPotential>
    <backgroundColor>-1</backgroundColor>
    <eventType>Exercise</eventType>
    <surpressRoomValidation>True</surpressRoomValidation>
    <staffComment></staffComment>
    <taskType></taskType>
    <taskParameters></taskParameters>
    <Bizur />
    <Groups />
    <Tracks />
    <Classes />
  </LessonInfo>
</WeekConfig>"""
    lesson = parse_lesson(xml)
    assert lesson.is_break is True
    assert lesson.is_skippable is True
    assert lesson.is_locked is True
    assert lesson.is_conversation_potential is True
    assert lesson.suppress_room_validation is True


def test_serialize_round_trip(sample_lesson_exercise):
    serialized = serialize_lesson(sample_lesson_exercise)
    parsed = parse_lesson(serialized)
    assert parsed.lesson_id == sample_lesson_exercise.lesson_id
    assert parsed.array == sample_lesson_exercise.array
    assert parsed.subject == sample_lesson_exercise.subject
    assert parsed.start_time == sample_lesson_exercise.start_time
    assert parsed.wanted_length == sample_lesson_exercise.wanted_length
    assert parsed.actual_length == sample_lesson_exercise.actual_length
    assert parsed.display == sample_lesson_exercise.display
    assert parsed.is_break == sample_lesson_exercise.is_break
    assert parsed.background_color == sample_lesson_exercise.background_color
    assert parsed.groups == sample_lesson_exercise.groups
    assert parsed.tracks == sample_lesson_exercise.tracks
    assert parsed.classes == sample_lesson_exercise.classes
    assert parsed.staff_comment == sample_lesson_exercise.staff_comment


def test_serialize_round_trip_break(sample_lesson_break):
    serialized = serialize_lesson(sample_lesson_break)
    parsed = parse_lesson(serialized)
    assert parsed.lesson_id == sample_lesson_break.lesson_id
    assert parsed.is_break is True
    assert parsed.background_color == -1


def test_empty_fields_preserved():
    lesson = Lesson(
        lesson_id=1,
        start_time=datetime(2026, 3, 17, 8, 0, 0),
        wanted_length=timedelta(hours=1),
        actual_length=timedelta(hours=1),
        master_id="",
        task_type="",
        task_parameters="",
    )
    serialized = serialize_lesson(lesson)
    parsed = parse_lesson(serialized)
    assert parsed.master_id == ""
    assert parsed.task_type == ""
    assert parsed.task_parameters == ""


def test_serialize_contains_lesson_id(sample_lesson_break):
    xml = serialize_lesson(sample_lesson_break)
    assert 'lessonId="1042328123"' in xml


def test_serialize_duration_format():
    lesson = Lesson(
        lesson_id=1,
        start_time=datetime(2026, 3, 17, 8, 0, 0),
        wanted_length=timedelta(hours=1, minutes=15),
        actual_length=timedelta(hours=1, minutes=15),
    )
    xml = serialize_lesson(lesson)
    assert "<lessonWantedLength>01:15:00</lessonWantedLength>" in xml
