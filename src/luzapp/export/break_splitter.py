from luzapp.models.lesson import Lesson


def split_lessons_and_breaks(items: list[Lesson]) -> list[Lesson]:
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
