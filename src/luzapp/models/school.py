from datetime import time, timedelta
from typing import Literal
from pydantic import BaseModel, ConfigDict
from luzapp.models.color import NamedColor


class Group(BaseModel):
    """A student group within a school cohort.

    Args:
        name: Unique name of the group.
        size: Number of students in the group.
    """

    model_config = ConfigDict(frozen=True)
    name: str
    size: int


class Track(BaseModel):
    """A curriculum track that groups lessons across multiple cohorts.

    Args:
        name: Unique name of the track.
    """

    model_config = ConfigDict(frozen=True)
    name: str


class ClassRoom(BaseModel):
    """A physical classroom or lab.

    Args:
        name: Unique name of the room.
        seats: Total seating capacity.
        workstations: Number of computer workstations available.
    """

    model_config = ConfigDict(frozen=True)
    name: str
    seats: int
    workstations: int


class Person(BaseModel):
    """A staff member.

    Args:
        name: Full name of the person.
        sex: ``"male"`` or ``"female"``.
    """

    model_config = ConfigDict(frozen=True)
    name: str
    sex: str  # "male" or "female"


class StaffGroup(BaseModel):
    """A named group of staff members (e.g. instructors, coordinators).

    Args:
        name: Display name for the group.
        members: Tuple of :class:`Person` objects belonging to the group.
    """

    model_config = ConfigDict(frozen=True)
    name: str
    members: tuple[Person, ...]


class SchoolConfig(BaseModel):
    """Static configuration for a school, parsed from ``config.school``.

    This model is the authoritative source for all school-wide settings:
    groups, tracks, classrooms, staff, and scheduling parameters.

    Args:
        name: Display name of the school / course.
        sync_server: URL of the LuzApp sync server for this school.
        groups: All student groups defined in the school.
        tracks: All curriculum tracks defined in the school.
        classes: All classrooms defined in the school.
        staff_groups: Named groups of staff members.
        default_class: Name of the default classroom.
        week_days: Number of school days in a week.
        day_start: Time at which the school day begins.
        day_length: Total duration of the school day.
        time_grid: Ordered tuple of lesson start times used by the scheduler.
        colors: Named colours used for schedule display.
    """

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

    def color_by_name(self, name: str) -> NamedColor | None:
        """Return the :class:`NamedColor` with the given name, or ``None``."""
        for c in self.colors:
            if c.name == name:
                return c
        return None

    def color_by_argb(self, argb_int: int) -> NamedColor | None:
        """Return the :class:`NamedColor` matching the given .NET ARGB int, or ``None``."""
        for c in self.colors:
            if c.to_argb_int() == argb_int:
                return c
        return None

    def find_group(self, name: str) -> Group | None:
        """Return the :class:`Group` with the given name, or ``None``."""
        for g in self.groups:
            if g.name == name:
                return g
        return None

    def all_staff(self) -> list[Person]:
        """Return a flat list of every :class:`Person` across all staff groups."""
        result = []
        for sg in self.staff_groups:
            result.extend(sg.members)
        return result
