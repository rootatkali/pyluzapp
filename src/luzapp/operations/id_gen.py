import random


def generate_lesson_id() -> int:
    return random.randint(1, 2**31 - 1)
