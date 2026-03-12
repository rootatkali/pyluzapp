from datetime import datetime, timedelta
from pathlib import Path
import pytest
from luzapp.models.lesson import Lesson
from luzapp.operations.lesson_ops import load_all_lessons, save_lesson, delete_lesson


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
WEEK01_DIR = FIXTURES_DIR / "weeks" / "week01"


def test_load_all_lessons():
    lessons = load_all_lessons(WEEK01_DIR)
    assert len(lessons) == 2
    ids = {l.lesson_id for l in lessons}
    assert 1042328123 in ids
    assert 1076807964 in ids


def test_load_all_lessons_no_obj_dir(tmp_path):
    week_dir = tmp_path / "week99"
    week_dir.mkdir()
    with pytest.raises(FileNotFoundError):
        load_all_lessons(week_dir)


def test_save_lesson(tmp_path):
    week_dir = tmp_path / "week01"
    lesson = Lesson(
        lesson_id=999001,
        start_time=datetime(2026, 3, 17, 8, 0, 0),
        wanted_length=timedelta(minutes=45),
        actual_length=timedelta(minutes=45),
        array="Test",
        display="Test Lesson",
    )
    path = save_lesson(week_dir, lesson)
    assert path.exists()
    assert path.name == "999001.luzngl"
    assert path.parent.name == "_obj"


def test_save_then_load(tmp_path):
    week_dir = tmp_path / "week01"
    lesson = Lesson(
        lesson_id=999002,
        start_time=datetime(2026, 3, 17, 9, 0, 0),
        wanted_length=timedelta(hours=1),
        actual_length=timedelta(hours=1),
        array="SaveTest",
        display="Save Test",
        groups=("GroupA",),
    )
    save_lesson(week_dir, lesson)
    lessons = load_all_lessons(week_dir)
    assert len(lessons) == 1
    loaded = lessons[0]
    assert loaded.lesson_id == 999002
    assert loaded.array == "SaveTest"
    assert loaded.groups == ("GroupA",)


def test_delete_lesson(tmp_path):
    week_dir = tmp_path / "week01"
    lesson = Lesson(
        lesson_id=999003,
        start_time=datetime(2026, 3, 17, 10, 0, 0),
        wanted_length=timedelta(minutes=30),
        actual_length=timedelta(minutes=30),
    )
    save_lesson(week_dir, lesson)
    delete_lesson(week_dir, 999003)
    obj_dir = week_dir / "_obj"
    assert not (obj_dir / "999003.luzngl").exists()


def test_delete_lesson_not_found(tmp_path):
    week_dir = tmp_path / "week01"
    (week_dir / "_obj").mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        delete_lesson(week_dir, 999999)
