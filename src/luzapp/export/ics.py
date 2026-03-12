import json
from datetime import datetime, timedelta
from uuid import uuid4

from luzapp.models.lesson import Lesson
from luzapp.translations.base import Translator
from luzapp.translations.dict_translator import NullTranslator
from luzapp.export.break_splitter import split_lessons_and_breaks

ICAL_HEADER = """BEGIN:VCALENDAR
PRODID:-//Microsoft Corporation//Outlook 14.0 MIMEDIR//EN
VERSION:2.0
METHOD:PUBLISH
X-WR-CALNAME:Luz
X-WR-RELCALID:{0000002E-09B4-D0B5-4082-6806A7D84CA9}
X-CALSTART:20110101T000000Z
BEGIN:VTIMEZONE
TZID:Israel Standard Time
BEGIN:STANDARD
DTSTART:16010916T020000
RRULE:FREQ=YEARLY;BYDAY=3SU;BYMONTH=9
TZOFFSETFROM:+0200
TZOFFSETTO:+0200
END:STANDARD
BEGIN:DAYLIGHT
DTSTART:16010330T020000
RRULE:FREQ=YEARLY;BYDAY=-1FR;BYMONTH=3
TZOFFSETFROM:+0200
TZOFFSETTO:+0200
END:DAYLIGHT
END:VTIMEZONE
"""

ICAL_EVENT_TEMPLATE = """BEGIN:VEVENT
CLASS:PUBLIC
CREATED:{created}
DESCRIPTION:{description}
DTEND;{dtend}
DTSTAMP:{created}
DTSTART;{dtstart}
LAST-MODIFIED:{created}
LOCATION:{location}
PRIORITY:5
SEQUENCE:0
SUMMARY;LANGUAGE=he:{summary}
{attendees}TRANSP:OPAQUE
UID:{uid}
X-MICROSOFT-CDO-BUSYSTATUS:BUSY
X-MICROSOFT-CDO-IMPORTANCE:1
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:Reminder
END:VALARM
END:VEVENT
"""

ICAL_DATE_FORMAT = "%Y%m%dT%H%M%SZ"
TZ_DATE_FORMAT = "%Y%m%dT%H%M%S"


def _tz_datetime(dt: datetime) -> str:
    return 'TZID="Israel Standard Time":' + dt.strftime(TZ_DATE_FORMAT)


def _get_summary(lesson: Lesson, translator: Translator) -> str:
    array = translator.translate_subject(lesson.array)

    if array == "הפסקה" or lesson.display in ["פתיחת יום", "סיכום יום"]:
        return lesson.display

    if array == "שונות":
        return f"הרצאה - {lesson.display}"

    if lesson.is_lecture:
        summary = "הרצאה - " + array
    else:
        summary = "עע - " + array

    if lesson.subject and array not in ["אג"]:
        summary += " - " + lesson.subject

    return summary


def _get_attendees(lesson: Lesson, translator: Translator) -> str:
    output = ""
    for group in lesson.groups:
        email = translator.translate_group(group)
        if email:
            display = email.split("@")[0]
            output += f"ATTENDEE;CN={display};RSVP=TRUE:mailto:{email}\n"
    return output


def export_ics(
    lessons: list[Lesson],
    translator: Translator | None = None,
    split_breaks: bool = True,
) -> str:
    if translator is None:
        translator = NullTranslator()

    items = split_lessons_and_breaks(lessons) if split_breaks else lessons

    created = (datetime.now() - timedelta(days=10)).strftime(ICAL_DATE_FORMAT)
    output = ICAL_HEADER

    for lesson in items:
        if "Hidden" in lesson.bizur:
            continue

        description = json.dumps({
            "distributed": list(lesson.bizur),
            "display": lesson.display,
            "subject": lesson.subject,
            "array": translator.translate_subject(lesson.array),
            "groups": list(lesson.groups),
            "tracks": list(lesson.tracks),
            "is_exercise": not lesson.is_lecture,
            "is_break": lesson.is_break,
            "is_lecture": lesson.is_lecture,
        })

        output += ICAL_EVENT_TEMPLATE.format(
            created=created,
            description=description,
            dtend=_tz_datetime(lesson.end_time),
            dtstart=_tz_datetime(lesson.start_time),
            location=", ".join(lesson.classes),
            summary=_get_summary(lesson, translator),
            attendees=_get_attendees(lesson, translator),
            uid=uuid4(),
        )

    output += "END:VCALENDAR"
    return output
