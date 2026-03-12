from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WeekConfig(BaseModel):
    """Configuration for a single scheduled week.

    Each week lives in its own subdirectory (``weeks/week{NN}/``) and has a
    corresponding ``.luzng`` XML file alongside the ``_obj/`` directory of
    lesson files.

    Args:
        number: Sequential week number (1-based).
        days_in_week: Number of school days in this particular week (may differ
            from the school-wide default, e.g. for shortened weeks).
        start_time: Datetime of the first moment of the week's first day.
        groups: Names of the student groups participating in this week.
        tracks: Names of the tracks active during this week.
        classes: Names of the classrooms in use during this week.
    """

    model_config = ConfigDict(frozen=True)

    number: int
    days_in_week: int
    start_time: datetime
    groups: tuple[str, ...]
    tracks: tuple[str, ...]
    classes: tuple[str, ...]
