from pathlib import Path
import pytest
from luzapp.serializers.school_serializer import parse_school


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
SCHOOL_FILE = FIXTURES_DIR / "config.school"


def test_parse_school_name():
    school = parse_school(SCHOOL_FILE)
    assert school.name == "Titan24"
    assert school.sync_server == "gitlab.com"


def test_parse_groups():
    school = parse_school(SCHOOL_FILE)
    assert len(school.groups) == 3
    names = [g.name for g in school.groups]
    assert "ונוס" in names
    venus = school.find_group("ונוס")
    assert venus is not None
    assert venus.size == 11


def test_parse_tracks():
    school = parse_school(SCHOOL_FILE)
    assert len(school.tracks) >= 2
    names = [t.name for t in school.tracks]
    assert "ונוס" in names


def test_parse_classes():
    school = parse_school(SCHOOL_FILE)
    assert len(school.classes) >= 2
    names = [c.name for c in school.classes]
    assert "ונוס" in names


def test_parse_default_class():
    school = parse_school(SCHOOL_FILE)
    assert school.default_class == "Teams"


def test_parse_week_days():
    school = parse_school(SCHOOL_FILE)
    assert school.week_days == 6


def test_parse_day_start():
    from datetime import time
    school = parse_school(SCHOOL_FILE)
    assert school.day_start == time(7, 50)


def test_parse_colors():
    school = parse_school(SCHOOL_FILE)
    assert len(school.colors) > 0
    names = [c.name for c in school.colors]
    assert "אדום" in names
    assert "לבן" in names


def test_color_by_name():
    school = parse_school(SCHOOL_FILE)
    red = school.color_by_name("אדום")
    assert red is not None
    assert red.r == 255
    assert red.g == 0
    assert red.b == 0


def test_color_by_name_white():
    school = parse_school(SCHOOL_FILE)
    white = school.color_by_name("לבן")
    assert white is not None
    assert white.to_argb_int() == -1


def test_color_by_argb():
    school = parse_school(SCHOOL_FILE)
    white = school.color_by_argb(-1)
    assert white is not None
    assert white.name == "לבן"


def test_parse_staff_groups():
    school = parse_school(SCHOOL_FILE)
    assert len(school.staff_groups) > 0
    names = [sg.name for sg in school.staff_groups]
    assert "סגל מוביל" in names


def test_all_staff():
    school = parse_school(SCHOOL_FILE)
    staff = school.all_staff()
    assert len(staff) > 0
    person_names = [p.name for p in staff]
    assert "Hidden" in person_names


def test_parse_time_grid():
    school = parse_school(SCHOOL_FILE)
    assert len(school.time_grid) > 0
