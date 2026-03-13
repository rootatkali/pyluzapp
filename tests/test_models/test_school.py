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


# --- with_*/without_* mutation helpers ---

def test_with_group_adds():
    school = make_school()
    new_group = Group(name="GroupB", size=20)
    updated = school.with_group(new_group)
    assert school is not updated
    assert len(updated.groups) == 2
    assert updated.find_group("GroupB") is not None


def test_with_group_replaces_same_name():
    school = make_school()
    replacement = Group(name="GroupA", size=99)
    updated = school.with_group(replacement)
    assert len(updated.groups) == 1
    assert updated.find_group("GroupA").size == 99


def test_without_group_removes():
    school = make_school()
    updated = school.without_group("GroupA")
    assert len(updated.groups) == 0


def test_without_group_noop_on_missing():
    school = make_school()
    updated = school.without_group("NonExistent")
    assert len(updated.groups) == 1


def test_with_track_adds():
    school = make_school()
    updated = school.with_track(Track(name="TrackB"))
    assert len(updated.tracks) == 2


def test_with_track_replaces():
    school = make_school()
    updated = school.with_track(Track(name="TrackA"))
    assert len(updated.tracks) == 1


def test_without_track_removes():
    school = make_school()
    updated = school.without_track("TrackA")
    assert len(updated.tracks) == 0


def test_with_class_adds():
    school = make_school()
    updated = school.with_class(ClassRoom(name="RoomB", seats=20, workstations=5))
    assert len(updated.classes) == 2


def test_with_class_replaces():
    school = make_school()
    updated = school.with_class(ClassRoom(name="RoomA", seats=50, workstations=20))
    assert len(updated.classes) == 1
    assert updated.classes[0].seats == 50


def test_without_class_removes():
    school = make_school()
    updated = school.without_class("RoomA")
    assert len(updated.classes) == 0


def test_with_color_adds():
    school = make_school()
    updated = school.with_color(NamedColor(name="blue", r=0, g=0, b=255))
    assert len(updated.colors) == 3


def test_with_color_replaces():
    school = make_school()
    updated = school.with_color(NamedColor(name="red", r=200, g=0, b=0))
    assert len(updated.colors) == 2
    assert updated.color_by_name("red").r == 200


def test_without_color_removes():
    school = make_school()
    updated = school.without_color("red")
    assert len(updated.colors) == 1
    assert updated.color_by_name("red") is None


def test_with_staff_group_adds():
    school = make_school()
    sg = StaffGroup(name="NewTeam", members=(Person(name="Alice", sex="female"),))
    updated = school.with_staff_group(sg)
    assert len(updated.staff_groups) == 1


def test_with_staff_group_replaces():
    existing_sg = StaffGroup(name="Team", members=(Person(name="Alice", sex="female"),))
    school = make_school(staff_groups=(existing_sg,))
    replacement = StaffGroup(name="Team", members=(Person(name="Bob", sex="male"),))
    updated = school.with_staff_group(replacement)
    assert len(updated.staff_groups) == 1
    assert updated.staff_groups[0].members[0].name == "Bob"


def test_without_staff_group_removes():
    sg = StaffGroup(name="Team", members=())
    school = make_school(staff_groups=(sg,))
    updated = school.without_staff_group("Team")
    assert len(updated.staff_groups) == 0


def test_mutation_helpers_return_new_instances():
    school = make_school()
    updated = school.with_group(Group(name="GroupB", size=5))
    assert updated is not school
    assert len(school.groups) == 1  # original unchanged
