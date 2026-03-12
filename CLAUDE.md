# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` for dependency management and task running.

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_models/test_lesson.py

# Run a single test
uv run pytest tests/test_models/test_lesson.py::test_name

# Run tests with coverage
uv run pytest --cov=src/luzapp

# Run linting (if configured)
uv run ruff check src/
```

## Architecture

This is a **generic Python library** (`luzapp`) for managing school schedules stored in a file-based git repository. It is designed to be used by school-specific projects that import the library and provide their own translations.

### Package structure

- **`src/luzapp/`** — the main library package
  - **`models/`** — immutable Pydantic models (`frozen=True`): `Lesson`, `SchoolConfig`, `WeekConfig`, `Group`, `Track`, `ClassRoom`, `Person`, `StaffGroup`, `NamedColor`
  - **`serializers/`** — XML serialization/deserialization for `.luzngl` (lesson) and `.luzng` (week/school) files
  - **`operations/`** — file I/O for lessons and weeks; ID generation
  - **`translations/`** — `Translator` ABC + `DictTranslator`/`NullTranslator` implementations for mapping subject codes and group names
  - **`export/`** — ICS calendar export; break splitter that splits long break slots
  - **`repo.py`** — `ScheduleRepo`: the primary entry point; takes a `root_path` and exposes all operations
  - **`git.py`** — thin wrappers around `git pull`, `git push`, `git status` via `subprocess`

### On-disk repository layout

A "schedule repository" (the `root_path` passed to `ScheduleRepo`) is structured as:

```
<root>/
  config.school          # SchoolConfig XML
  weeks/
    week01/
      week01.luzng       # WeekConfig XML
      _obj/
        <id>.luzngl      # one file per Lesson XML
    week02/
      ...
```

### Key design decisions

- All models are **immutable** Pydantic models (`ConfigDict(frozen=True)`). Use `model.model_copy(update={...})` to produce modified copies.
- The `Translator` ABC is the extension point for school-specific subject/group name mappings. Implement it in school-specific packages; pass it to `export_ics()`.
- `ScheduleRepo` is the **only** public API consumers should use — it composes serializers, operations, and exports.
- Lesson files use a custom XML format compatible with the LuzApp .NET application (field names like `lessonIsBreak`, `backgroundColor`, `surpressRoomValidation` must match exactly).
- `background_color` is stored as a .NET ARGB signed int.
