from datetime import datetime
from pathlib import Path
import pytest
from luzapp.repo import ScheduleRepo
from luzapp.models.week import WeekConfig
from luzapp.models.lesson import Lesson
from datetime import timedelta


FIXTURES_DIR = Path(__file__).parent / "fixtures"


def test_repo_construction(venus_repo):
    assert venus_repo.root_path == FIXTURES_DIR


def test_repo_raises_on_missing_config(tmp_path):
    with pytest.raises(FileNotFoundError):
        ScheduleRepo(tmp_path)


def test_school_config_lazy_loads(venus_repo):
    school = venus_repo.school_config
    assert school.name == "Titan24"


def test_school_config_cached(venus_repo):
    school1 = venus_repo.school_config
    school2 = venus_repo.school_config
    assert school1 is school2


def test_list_weeks(venus_repo):
    weeks = venus_repo.list_weeks()
    assert 1 in weeks


def test_get_week(venus_repo):
    week = venus_repo.get_week(1)
    assert week.number == 1
    assert week.groups == ("ונוס",)


def test_get_lessons(venus_repo):
    lessons = venus_repo.get_lessons(1)
    assert len(lessons) == 2
    ids = {l.lesson_id for l in lessons}
    assert 1042328123 in ids
    assert 1076807964 in ids


def test_create_week(tmp_path):
    # Copy config.school to tmp_path for repo usage
    import shutil
    shutil.copy(FIXTURES_DIR / "config.school", tmp_path / "config.school")
    repo = ScheduleRepo(tmp_path)
    week = WeekConfig(
        number=1,
        days_in_week=6,
        start_time=datetime(2026, 3, 15, 0, 0, 0),
        groups=("ונוס",),
        tracks=("ונוס",),
        classes=("ונוס",),
    )
    week_dir = repo.create_week(week)
    assert week_dir.is_dir()
    assert 1 in repo.list_weeks()


def test_save_and_get_lessons(tmp_path):
    import shutil
    shutil.copy(FIXTURES_DIR / "config.school", tmp_path / "config.school")
    repo = ScheduleRepo(tmp_path)
    week = WeekConfig(
        number=2,
        days_in_week=6,
        start_time=datetime(2026, 3, 22, 0, 0, 0),
        groups=("ונוס",),
        tracks=(),
        classes=(),
    )
    repo.create_week(week)
    lesson = Lesson(
        lesson_id=12345,
        start_time=datetime(2026, 3, 22, 8, 0, 0),
        wanted_length=timedelta(hours=1),
        actual_length=timedelta(hours=1),
        array="Test",
        display="Test Lesson",
        groups=("ונוס",),
    )
    repo.save_lesson(2, lesson)
    lessons = repo.get_lessons(2)
    assert len(lessons) == 1
    assert lessons[0].lesson_id == 12345


def test_delete_lesson(tmp_path):
    import shutil
    shutil.copy(FIXTURES_DIR / "config.school", tmp_path / "config.school")
    repo = ScheduleRepo(tmp_path)
    week = WeekConfig(
        number=3,
        days_in_week=6,
        start_time=datetime(2026, 3, 29, 0, 0, 0),
        groups=(),
        tracks=(),
        classes=(),
    )
    repo.create_week(week)
    lesson = Lesson(
        lesson_id=99999,
        start_time=datetime(2026, 3, 29, 8, 0, 0),
        wanted_length=timedelta(minutes=30),
        actual_length=timedelta(minutes=30),
    )
    repo.save_lesson(3, lesson)
    repo.delete_lesson(3, 99999)
    lessons = repo.get_lessons(3)
    assert len(lessons) == 0


def test_generate_lesson_id(venus_repo):
    lid = venus_repo.generate_lesson_id()
    assert isinstance(lid, int)
    assert 1 <= lid <= 2**31 - 1


def test_export_ics(venus_repo):
    result = venus_repo.export_ics([1])
    assert "BEGIN:VCALENDAR" in result
    assert "END:VCALENDAR" in result
