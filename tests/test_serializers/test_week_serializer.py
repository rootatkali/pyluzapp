from datetime import datetime
from pathlib import Path
import pytest
from luzapp.serializers.week_serializer import parse_week, serialize_week
from luzapp.models.week import WeekConfig


FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
WEEK01_FILE = FIXTURES_DIR / "weeks" / "week01" / "week01.luzng"


def test_parse_week_from_file():
    week = parse_week(WEEK01_FILE)
    assert week.number == 1
    assert week.days_in_week == 6
    assert week.start_time == datetime(2026, 3, 15, 0, 0, 0)
    assert week.groups == ("ונוס",)
    assert week.tracks == ("ונוס",)
    assert week.classes == ("ונוס",)


def test_parse_week_from_string():
    xml = '<WeekConfig number="2" daysInWeek="5" startTime="22/03/2026 00:00:00"><Groups><Item>A</Item></Groups><Tracks /><Classes /></WeekConfig>'
    week = parse_week(xml)
    assert week.number == 2
    assert week.days_in_week == 5
    assert week.groups == ("A",)
    assert week.tracks == ()
    assert week.classes == ()


def test_serialize_round_trip():
    week = parse_week(WEEK01_FILE)
    serialized = serialize_week(week)
    recovered = parse_week(serialized)
    assert recovered.number == week.number
    assert recovered.days_in_week == week.days_in_week
    assert recovered.start_time == week.start_time
    assert recovered.groups == week.groups
    assert recovered.tracks == week.tracks
    assert recovered.classes == week.classes


def test_serialize_week_format():
    week = WeekConfig(
        number=3,
        days_in_week=6,
        start_time=datetime(2026, 3, 29, 0, 0, 0),
        groups=("GroupA", "GroupB"),
        tracks=("TrackA",),
        classes=("RoomA",),
    )
    xml = serialize_week(week)
    assert 'number="3"' in xml
    assert 'daysInWeek="6"' in xml
    assert "29/03/2026" in xml
    assert "<Item>GroupA</Item>" in xml
    assert "<Item>GroupB</Item>" in xml
