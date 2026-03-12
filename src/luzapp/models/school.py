from datetime import time, timedelta
from typing import Optional
from pydantic import BaseModel, ConfigDict
from luzapp.models.color import NamedColor


class Group(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    size: int


class Track(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str


class ClassRoom(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    seats: int
    workstations: int


class Person(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    sex: str  # "male" or "female"


class StaffGroup(BaseModel):
    model_config = ConfigDict(frozen=True)
    name: str
    members: tuple[Person, ...]


class SchoolConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    sync_server: str
    groups: tuple[Group, ...]
    tracks: tuple[Track, ...]
    classes: tuple[ClassRoom, ...]
    staff_groups: tuple[StaffGroup, ...]
    default_class: str
    week_days: int
    day_start: time
    day_length: timedelta
    time_grid: tuple[time, ...]
    colors: tuple[NamedColor, ...]

    def color_by_name(self, name: str) -> Optional[NamedColor]:
        for c in self.colors:
            if c.name == name:
                return c
        return None

    def color_by_argb(self, argb_int: int) -> Optional[NamedColor]:
        for c in self.colors:
            if c.to_argb_int() == argb_int:
                return c
        return None

    def find_group(self, name: str) -> Optional[Group]:
        for g in self.groups:
            if g.name == name:
                return g
        return None

    def all_staff(self) -> list[Person]:
        result = []
        for sg in self.staff_groups:
            result.extend(sg.members)
        return result
