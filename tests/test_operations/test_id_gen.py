from luzapp.operations.id_gen import generate_lesson_id


def test_generate_lesson_id_range():
    for _ in range(100):
        lid = generate_lesson_id()
        assert 1 <= lid <= 2**31 - 1


def test_generate_lesson_id_is_int():
    lid = generate_lesson_id()
    assert isinstance(lid, int)


def test_generate_lesson_id_unique():
    ids = {generate_lesson_id() for _ in range(50)}
    # With a 2^31 range, almost certainly unique
    assert len(ids) > 40
