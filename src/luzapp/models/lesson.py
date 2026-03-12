from datetime import datetime, timedelta, date
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, model_validator


EventType = Literal["Exercise", "Lecture"]

_BIZUR_HIDDEN = "Hidden"
_BIZUR_FAKE = "פיקטיבי"
_BIZUR_CRITICAL = "קריטי"


class Lesson(BaseModel):
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
    classes: tuple[str, ...]

    @model_validator(mode="before")
    @classmethod
    def _fold_bizur_flags(cls, data: Any) -> Any:
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
        return data = ()

    @property
    def end_time(self) -> datetime:
        return self.start_time + self.actual_length

    @property
    def date(self) -> date:
        return self.start_time.date()

    @property
    def is_lecture(self) -> bool:
        return self.event_type == "Lecture"

    @property
    def start_timedelta(self) -> timedelta:
        t = self.start_time.time()
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)

    @property
    def end_timedelta(self) -> timedelta:
        return self.start_timedelta + self.actual_length

    @property
    def is_hidden(self) -> bool:
        return _BIZUR_HIDDEN in self.bizur

    @property
    def is_fake(self) -> bool:
        return _BIZUR_FAKE in self.bizur

    @property
    def is_critical(self) -> bool:
        return _BIZUR_CRITICAL in self.bizur
