from datetime import datetime
import pytest
from luzapp.models.week import WeekConfig


def test_week_construction():
    week = WeekConfig(
        number=1,
        days_in_week=6,
        start_time=datetime(2026, 3, 15, 0, 0, 0),
        groups=("ונוס",),
        tracks=("ונוס",),
        classes=("ונוס",),
    )
    assert week.number == 1
    assert week.days_in_week == 6
    assert week.groups == ("ונוס",)


def test_week_frozen():
    week = WeekConfig(
        number=1,
        days_in_week=6,
        start_time=datetime(2026, 3, 15),
        groups=(),
        tracks=(),
        classes=(),
    )
    with pytest.raises(Exception):
        week.number = 2  # type: ignore


def test_week_model_copy():
    week = WeekConfig(
        number=1,
        days_in_week=6,
        start_time=datetime(2026, 3, 15),
        groups=("A",),
        tracks=(),
        classes=(),
    )
    updated = week.model_copy(update={"number": 2})
    assert week.number == 1
    assert updated.number == 2
    assert updated.groups == ("A",)
