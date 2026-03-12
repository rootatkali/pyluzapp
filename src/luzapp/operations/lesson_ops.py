from pathlib import Path
from luzapp.models.lesson import Lesson
from luzapp.serializers.lesson_serializer import parse_lesson, serialize_lesson

LUZ_EXTENSION = ".luzngl"
OBJ_DIR = "_obj"


def get_obj_dir(week_dir: Path) -> Path:
    """Return the path of the ``_obj`` directory within *week_dir*."""
    return week_dir / OBJ_DIR


def load_all_lessons(week_dir: Path) -> list[Lesson]:
    """Load every lesson from the ``_obj`` directory of a week.

    Args:
        week_dir: Path to the week directory (e.g. ``weeks/week01/``).

    Returns:
        A list of :class:`~luzapp.models.lesson.Lesson` objects in unspecified
        order.

    Raises:
        FileNotFoundError: If the ``_obj`` subdirectory does not exist.
    """
    obj_dir = get_obj_dir(week_dir)
    if not obj_dir.is_dir():
        raise FileNotFoundError(f"No _obj directory in {week_dir}")
    lessons = []
    for f in obj_dir.iterdir():
        if f.is_file() and f.suffix == LUZ_EXTENSION:
            lessons.append(parse_lesson(f))
    return lessons


def save_lesson(week_dir: Path, lesson: Lesson) -> Path:
    """Serialize and write a lesson to the ``_obj`` directory.

    The ``_obj`` directory is created if it does not exist.  An existing file
    with the same lesson ID is overwritten.

    Args:
        week_dir: Path to the week directory.
        lesson: Lesson to persist.

    Returns:
        The path of the written ``.luzngl`` file.
    """
    obj_dir = get_obj_dir(week_dir)
    obj_dir.mkdir(parents=True, exist_ok=True)
    path = obj_dir / f"{lesson.lesson_id}{LUZ_EXTENSION}"
    path.write_text(serialize_lesson(lesson), encoding="utf-8")
    return path


def delete_lesson(week_dir: Path, lesson_id: int) -> None:
    """Delete the ``.luzngl`` file for the given lesson ID.

    Args:
        week_dir: Path to the week directory.
        lesson_id: ID of the lesson to remove.

    Raises:
        FileNotFoundError: If no file exists for *lesson_id*.
    """
    path = get_obj_dir(week_dir) / f"{lesson_id}{LUZ_EXTENSION}"
    if not path.exists():
        raise FileNotFoundError(f"Lesson {lesson_id} not found in {week_dir}")
    path.unlink()
