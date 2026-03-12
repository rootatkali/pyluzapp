import random


def generate_lesson_id() -> int:
    """Generate a random positive lesson ID compatible with LuzApp.

    Returns a random integer in the range ``[1, 2³¹ − 1]``, matching the
    signed 32-bit integer range used by LuzApp for lesson identifiers.
    """
    return random.randint(1, 2**31 - 1)
