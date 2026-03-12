from datetime import time, timedelta
import pytest
from luzapp.models.school import SchoolConfig, Group, Track, ClassRoom, StaffGroup, Person
from luzapp.models.color import NamedColor


def make_school(**kwargs) -> SchoolConfig:
    defaults = dict(
        name="TestSchool",
        sync_server="github.com",
        groups=(Group(name="GroupA", size=10),),
        tracks=(Track(name="TrackA"),),
        classes=(ClassRoom(name="RoomA", seats=30, workstations=10),),
        staff_groups=(),
        default_class="Teams",
        week_days=6,
        day_start=time(8, 0),
        day_length=timedelta(hours=12),
        time_grid=(),
        colors=(
            NamedColor(name="red", r=255, g=0, b=0),
            NamedColor(name="white", r=255, g=255, b=255),
        ),
    )
    defaults.update(kwargs)
    return SchoolConfig(**defaults)


def test_school_construction():
    school = make_school()
    assert school.name == "TestSchool"
    assert len(school.groups) == 1


def test_color_by_name_found():
    school = make_school()
    color = school.color_by_name("red")
    assert color is not None
    assert color.r == 255


def test_color_by_name_not_found():
    school = make_school()
    assert school.color_by_name("nonexistent") is None


def test_color_by_argb():
    school = make_school()
    argb = NamedColor(name="white", r=255, g=255, b=255).to_argb_int()
    color = school.color_by_argb(argb)
    assert color is not None
    assert color.name == "white"


def test_color_by_argb_not_found():
    school = make_school()
    assert school.color_by_argb(9999999) is None


def test_find_group():
    school = make_school()
    group = school.find_group("GroupA")
    assert group is not None
    assert group.size == 10


def test_find_group_not_found():
    school = make_school()
    assert school.find_group("NonExistent") is None


def test_all_staff():
    staff_groups = (
        StaffGroup(
            name="Leaders",
            members=(
                Person(name="Alice", sex="female"),
                Person(name="Bob", sex="male"),
            ),
        ),
    )
    school = make_school(staff_groups=staff_groups)
    staff = school.all_staff()
    assert len(staff) == 2
    assert staff[0].name == "Alice"


def test_frozen():
    school = make_school()
    with pytest.raises(Exception):
        school.name = "mutated"  # type: ignore


def test_week_model():
    school = make_school()
    assert school.week_days == 6


def test_group_frozen():
    g = Group(name="G", size=5)
    with pytest.raises(Exception):
        g.name = "mutated"  # type: ignore
