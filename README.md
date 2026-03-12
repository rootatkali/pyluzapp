# pyluzapp

Python library for reading and writing LuzApp schedule repositories.

A LuzApp schedule repository is a git-tracked directory of XML files that LuzApp uses to store and sync school timetables. This library lets you read, modify, and export those schedules from Python without running LuzApp itself.

## Installation

```bash
# TODO: Add local repository instructions
pip install luzapp
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
# TODO: Add local repository instructions
uv add luzapp
```

**Requires Python 3.13+.**

## Quick start

```python
from luzapp import ScheduleRepo

repo = ScheduleRepo("/path/to/school-repo")

# List available weeks
print(repo.list_weeks())  # [1, 2, 3, ...]

# Load lessons for a week
lessons = repo.get_lessons(week_number=1)
for lesson in lessons:
    print(lesson.start_time, lesson.array, lesson.display)

# Export weeks 1–3 to an iCalendar file
ics = repo.export_ics([1, 2, 3])
with open("schedule.ics", "w", encoding="utf-8") as f:
    f.write(ics)
```

## Repository layout

The library expects a directory with the following structure:

```
<root>/
  config.school          # school configuration (XML)
  weeks/
    week01/
      week01.luzng       # week configuration (XML)
      _obj/
        <id>.luzngl      # one file per lesson (XML)
    week02/
      ...
```

The `weeks/` directory name and `config.school` filename are configurable:

```python
repo = ScheduleRepo(root_path, config_file="school.xml", weeks_dir="schedule")
```

## Translations

Subject codes and group names are school-specific. Implement `Translator` in your school package to map them:

```python
from luzapp import DictTranslator

translator = DictTranslator(
    subjects={"MATH": "Mathematics", "ENG": "English"},
    groups={"AlphaGroup": "alpha@school.example.com"},
)

ics = repo.export_ics([1, 2], translator=translator)
```

`DictTranslator` covers simple lookup tables. For more complex logic, subclass `luzapp.Translator` directly.

## Creating and modifying lessons

All models are immutable. Use `model_copy(update={...})` to produce a modified copy, then save it:

```python
from luzapp import Lesson
from datetime import datetime, timedelta

lesson = Lesson(
    lesson_id=repo.generate_lesson_id(),
    array="MATH",
    subject="Algebra",
    start_time=datetime(2026, 3, 16, 9, 0),
    wanted_length=timedelta(hours=1),
    actual_length=timedelta(hours=1),
    groups=("Alpha",),
    is_critical=True,   # adds "קריטי" to the bizur tags
)

repo.save_lesson(week_number=1, lesson=lesson)
```

### Bizur flags

Three scheduling tags can be set via constructor kwargs or read as properties:

| Property | Bizur tag | Meaning |
|---|---|---|
| `is_hidden` | `Hidden` | Excluded from exports and consumer views |
| `is_fake` | `פיקטיבי` | Placeholder concealing a real event |
| `is_critical` | `קריטי` | Marked as critical |

## Syncing via git

```python
from luzapp import git

git.git_pull("/path/to/school-repo")
# ... make changes ...
git.git_push("/path/to/school-repo", message="update week 5")
```

## Development

```bash
uv sync
uv run pytest
uv run pytest --cov=src/luzapp   # with coverage
```
