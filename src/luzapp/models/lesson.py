from datetime import datetime, timedelta
from typing import Literal
from pydantic import BaseModel, ConfigDict


EventType = Literal["Exercise", "Lecture"]


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
    classes: tuple[str, ...] = ()

    @property
    def end_time(self) -> datetime:
        return self.start_time + self.actual_length

    @property
    def date(self):
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
