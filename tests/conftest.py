from pathlib import Path
import pytest
from luzapp.repo import ScheduleRepo
from luzapp.serializers.lesson_serializer import parse_lesson


FIXTURES_DIR = Path(__file__).parent / "fixtures"
WEEK01_OBJ_DIR = FIXTURES_DIR / "weeks" / "week01" / "_obj"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR


@pytest.fixture
def venus_repo() -> ScheduleRepo:
    return ScheduleRepo(FIXTURES_DIR)


@pytest.fixture
def sample_lesson_break():
    return parse_lesson(WEEK01_OBJ_DIR / "1042328123.luzngl")


@pytest.fixture
def sample_lesson_exercise():
    return parse_lesson(WEEK01_OBJ_DIR / "1076807964.luzngl")
