from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WeekConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    number: int
    days_in_week: int
    start_time: datetime
    groups: tuple[str, ...]
    tracks: tuple[str, ...]
    classes: tuple[str, ...]
