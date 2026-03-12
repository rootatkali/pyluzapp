from pathlib import Path
from luzapp.models.week import WeekConfig
from luzapp.serializers.week_serializer import serialize_week, parse_week

OBJ_DIR = "_obj"


def week_dir_name(number: int) -> str:
    return f"week{number:02d}"


def get_week_dir(weeks_path: Path, number: int) -> Path:
    return weeks_path / week_dir_name(number)


def get_week_file(week_dir: Path) -> Path:
    return week_dir / f"{week_dir.name}.luzng"


def list_weeks(weeks_path: Path) -> list[int]:
    if not weeks_path.is_dir():
        return []
    numbers = []
    for d in weeks_path.iterdir():
        if d.is_dir() and d.name.startswith("week"):
            try:
                numbers.append(int(d.name[4:]))
            except ValueError:
                continue
    return sorted(numbers)


def create_week(weeks_path: Path, week_config: WeekConfig) -> Path:
    week_dir = get_week_dir(weeks_path, week_config.number)
    week_dir.mkdir(parents=True, exist_ok=True)
    (week_dir / OBJ_DIR).mkdir(exist_ok=True)
    week_file = get_week_file(week_dir)
    week_file.write_text(serialize_week(week_config), encoding="utf-8")
    return week_dir


def load_week(weeks_path: Path, number: int) -> WeekConfig:
    week_dir = get_week_dir(weeks_path, number)
    week_file = get_week_file(week_dir)
    if not week_file.exists():
        raise FileNotFoundError(f"Week {number} not found at {week_file}")
    return parse_week(week_file)
