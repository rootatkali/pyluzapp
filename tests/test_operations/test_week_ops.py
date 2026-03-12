from datetime import datetime
from pathlib import Path
import pytest
from luzapp.models.week import WeekConfig
from luzapp.operations.week_ops import (
    create_week,
    list_weeks,
    load_week,
    get_week_dir,
    week_dir_name,
)


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def make_week(number: int = 1) -> WeekConfig:
    return WeekConfig(
        number=number,
        days_in_week=6,
        start_time=datetime(2026, 3, 15, 0, 0, 0),
        groups=("ונוס",),
        tracks=("ונוס",),
        classes=("ונוס",),
    )


def test_week_dir_name():
    assert week_dir_name(1) == "week01"
    assert week_dir_name(10) == "week10"


def test_create_week(tmp_path):
    week = make_week(1)
    week_dir = create_week(tmp_path, week)
    assert week_dir.is_dir()
    assert (week_dir / "_obj").is_dir()
    assert (week_dir / "week01.luzng").exists()


def test_create_week_file_content(tmp_path):
    week = make_week(2)
    week_dir = create_week(tmp_path, week)
    content = (week_dir / "week02.luzng").read_text(encoding="utf-8")
    assert 'number="2"' in content
    assert "ונוס" in content


def test_list_weeks_from_fixtures():
    weeks = list_weeks(FIXTURES_DIR)
    assert 1 in weeks


def test_list_weeks_empty(tmp_path):
    weeks = list_weeks(tmp_path)
    assert weeks == []


def test_list_weeks_sorted(tmp_path):
    for n in [3, 1, 2]:
        create_week(tmp_path, make_week(n))
    weeks = list_weeks(tmp_path)
    assert weeks == [1, 2, 3]


def test_load_week_from_fixtures():
    week = load_week(FIXTURES_DIR, 1)
    assert week.number == 1
    assert week.days_in_week == 6
    assert week.groups == ("ונוס",)


def test_load_week_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_week(tmp_path, 99)


def test_create_then_load(tmp_path):
    original = make_week(5)
    create_week(tmp_path, original)
    loaded = load_week(tmp_path, 5)
    assert loaded.number == original.number
    assert loaded.groups == original.groups
    assert loaded.start_time == original.start_time
