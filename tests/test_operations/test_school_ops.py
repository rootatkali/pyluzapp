from datetime import time, timedelta
from pathlib import Path
import pytest

from luzapp.models.school import SchoolConfig, Group, Track, ClassRoom, StaffGroup, Person
from luzapp.models.color import NamedColor
from luzapp.operations.school_ops import save_school
from luzapp.serializers.school_serializer import parse_school


def make_school(**kwargs) -> SchoolConfig:
    defaults = dict(
        name="TestSchool",
        sync_server="github.com",
        groups=(Group(name="GroupA", size=10),),
        tracks=(Track(name="TrackA"),),
        classes=(ClassRoom(name="RoomA", seats=30, workstations=10),),
        staff_groups=(
            StaffGroup(
                name="Leaders",
                members=(Person(name="Alice", sex="female"),),
            ),
        ),
        default_class="RoomA",
        week_days=5,
        day_start=time(8, 0),
        day_length=timedelta(hours=8),
        time_grid=(time(8, 0), time(9, 0), time(10, 0)),
        colors=(
            NamedColor(name="red", r=255, g=0, b=0),
            NamedColor(name="white", r=255, g=255, b=255),
        ),
    )
    defaults.update(kwargs)
    return SchoolConfig(**defaults)


def test_save_school_creates_file(tmp_path):
    config = make_school()
    dest = tmp_path / "config.school"
    save_school(dest, config)
    assert dest.exists()


def test_save_school_round_trips(tmp_path):
    config = make_school()
    dest = tmp_path / "config.school"
    save_school(dest, config)
    restored = parse_school(dest)

    assert restored.name == config.name
    assert restored.sync_server == config.sync_server
    assert restored.week_days == config.week_days
    assert restored.day_start == config.day_start
    assert restored.day_length == config.day_length
    assert restored.default_class == config.default_class
    assert len(restored.groups) == len(config.groups)
    assert restored.groups[0].name == config.groups[0].name
    assert restored.groups[0].size == config.groups[0].size
    assert len(restored.tracks) == len(config.tracks)
    assert len(restored.classes) == len(config.classes)
    assert len(restored.colors) == len(config.colors)
    assert len(restored.staff_groups) == len(config.staff_groups)
    assert restored.staff_groups[0].members[0].name == "Alice"
    assert len(restored.time_grid) == len(config.time_grid)


def test_save_school_overwrites_existing(tmp_path):
    original = make_school(name="Original")
    dest = tmp_path / "config.school"
    save_school(dest, original)

    updated = make_school(name="Updated")
    save_school(dest, updated)

    restored = parse_school(dest)
    assert restored.name == "Updated"
