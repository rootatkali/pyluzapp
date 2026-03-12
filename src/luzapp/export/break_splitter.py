from luzapp.models.lesson import Lesson


def split_lessons_and_breaks(items: list[Lesson]) -> list[Lesson]:
    """Split lessons that overlap a break slot into two separate events.

    Given a mixed list of lessons and breaks, this function ensures that no
    lesson spans across a break.  When a break falls in the middle of a lesson
    the lesson is replaced by two shorter copies: one ending at the break start
    and one starting at the break end.  Breaks are always preserved in the
    returned list.

    Breaks are processed in chronological order.  All times are assumed to be
    within the same calendar day; cross-midnight lessons are not supported.

    Args:
        items: A flat list of :class:`~luzapp.models.lesson.Lesson` objects,
            which may include both regular lessons and break slots
            (``is_break=True``).

    Returns:
        A new list containing the (possibly split) lessons followed by all
        break slots.  Order within the lesson portion is not guaranteed.
    """
    lessons = [i for i in items if not i.is_break]
    breaks = [i for i in items if i.is_break]

    result_lessons = list(lessons)

    for luz_break in sorted(breaks, key=lambda x: x.start_timedelta):
        break_start = luz_break.start_timedelta
        break_end = luz_break.end_timedelta

        new_lessons: list[Lesson] = []
        updated_lessons: list[Lesson] = []

        for lesson in result_lessons:
            lesson_start = lesson.start_timedelta
            lesson_end = lesson.end_timedelta

            if lesson_start < break_start < lesson_end:
                # Split: shorten original, create second part after break
                shortened = lesson.model_copy(update={
                    "actual_length": break_start - lesson_start,
                    "wanted_length": break_start - lesson_start,
                })
                after_break_start = lesson.start_time.replace(
                    hour=0, minute=0, second=0
                ) + break_end
                second_part = lesson.model_copy(update={
                    "start_time": after_break_start,
                    "actual_length": lesson_end - break_end,
                    "wanted_length": lesson_end - break_end,
                })
                updated_lessons.append(shortened)
                new_lessons.append(second_part)
            else:
                updated_lessons.append(lesson)

        result_lessons = updated_lessons + new_lessons

    return result_lessons + breaks
