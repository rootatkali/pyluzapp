from datetime import datetime, timedelta, date
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, model_validator


EventType = Literal["Exercise", "Lecture"]

_BIZUR_HIDDEN = "Hidden"
_BIZUR_FAKE = "פיקטיבי"
_BIZUR_CRITICAL = "קריטי"


class Lesson(BaseModel):
    """A single scheduled lesson or break in a LuzApp week.

    All fields are immutable after construction.  The ``bizur`` tuple holds
    internal scheduling tags used by LuzApp (e.g. ``"Hidden"``, ``"קריטי"``).
    Three of these tags are surfaced as convenience constructor flags and
    computed properties: ``is_hidden``, ``is_fake``, and ``is_critical``.

    Args:
        lesson_id: Unique integer identifier for this lesson.
        master_id: Reference to a master lesson template, if any.
        array: Subject area / course code (e.g. ``"MATH"``).
        subject: Specific topic or sub-subject within the array.
        start_time: Date and time at which the lesson begins.
        wanted_length: Originally planned duration.
        actual_length: Actual (possibly adjusted) duration.
        display: Human-readable display name shown on the schedule.
        is_break: Whether this entry represents a break slot.
        is_skippable: Whether groups not relevant to this lesson may skip it.
        is_locked: Whether the lesson is locked against rescheduling.
        is_conversation_potential: Whether this slot can be used for conversations.
        background_color: Display colour as a .NET ARGB signed integer.
        event_type: ``"Exercise"`` (default) or ``"Lecture"``.
        suppress_room_validation: Skip classroom capacity validation when ``True``.
        staff_comment: Internal comment visible only to staff.
        task_type: Type identifier for task-based lessons.
        task_parameters: Parameters string for task-based lessons.
        bizur: Tuple of scheduling tags assigned by LuzApp.
        groups: Names of the student groups attending this lesson.
        tracks: Names of the tracks this lesson belongs to.
        classes: Names of the classrooms used by this lesson.
        is_hidden: Convenience flag — adds ``"Hidden"`` to *bizur* when ``True``.
        is_fake: Convenience flag — adds ``"פיקטיבי"`` to *bizur* when ``True``.
        is_critical: Convenience flag — adds ``"קריטי"`` to *bizur* when ``True``.
    """

    model_config = ConfigDict(frozen=True)

    lesson_id: int
    master_id: str = ""
    array: str = ""
    subject: str = ""
    start_time: datetime
    wanted_length: timedelta
    actual_length: timedelta
    display: str = ""
    is_break: bool = False
    is_skippable: bool = False
    is_locked: bool = False
    is_conversation_potential: bool = False
    background_color: int = -1  # .NET ARGB signed int
    event_type: EventType = "Exercise"
    suppress_room_validation: bool = False
    staff_comment: str = ""
    task_type: str = ""
    task_parameters: str = ""
    bizur: tuple[str, ...] = ()
    groups: tuple[str, ...] = ()
    tracks: tuple[str, ...] = ()
    classes: tuple[str, ...] = ()

    @model_validator(mode="before")
    @classmethod
    def _fold_bizur_flags(cls, data: Any) -> Any:
        """Fold is_hidden/is_fake/is_critical kwargs into the bizur tuple."""
        if not isinstance(data, dict):
            return data
        flags = {
            "is_hidden": _BIZUR_HIDDEN,
            "is_fake": _BIZUR_FAKE,
            "is_critical": _BIZUR_CRITICAL,
        }
        extra = {k: data.pop(k, False) for k in flags}
        if any(extra.values()):
            bizur = set(data.get("bizur", ()))
            for key, tag in flags.items():
                if extra[key]:
                    bizur.add(tag)
            data["bizur"] = tuple(bizur)
        return data

    @property
    def end_time(self) -> datetime:
        """Datetime at which the lesson ends (``start_time + actual_length``)."""
        return self.start_time + self.actual_length

    @property
    def date(self) -> date:
        """Calendar date on which this lesson occurs."""
        return self.start_time.date()

    @property
    def is_lecture(self) -> bool:
        """``True`` when ``event_type`` is ``"Lecture"``."""
        return self.event_type == "Lecture"

    @property
    def start_timedelta(self) -> timedelta:
        """Time-of-day of ``start_time`` expressed as a :class:`timedelta` from midnight."""
        t = self.start_time.time()
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

    @property
    def end_timedelta(self) -> timedelta:
        """Time-of-day of ``end_time`` expressed as a :class:`timedelta` from midnight."""
        return self.start_timedelta + self.actual_length

    @property
    def is_hidden(self) -> bool:
        """``True`` when the ``"Hidden"`` bizur tag is set.

        Hidden lessons are excluded from ICS exports and other consumer views.
        """
        return _BIZUR_HIDDEN in self.bizur

    @property
    def is_fake(self) -> bool:
        """``True`` when the ``"פיקטיבי"`` (fake) bizur tag is set.

        Fake lessons are placeholder entries shown on the schedule to conceal
        a real event (e.g. a surprise outing).
        """
        return _BIZUR_FAKE in self.bizur

    @property
    def is_critical(self) -> bool:
        """``True`` when the ``"קריטי"`` (critical) bizur tag is set."""
        return _BIZUR_CRITICAL in self.bizur
