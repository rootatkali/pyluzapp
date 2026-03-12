import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

from luzapp.models.lesson import Lesson

DATE_FORMAT = "%d/%m/%Y %H:%M:%S"
DURATION_FORMAT = "{:02d}:{:02d}:{:02d}"


def _duration_to_str(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return DURATION_FORMAT.format(hours, minutes, seconds)


def _parse_duration(s: str) -> timedelta:
    parts = s.strip().split(":")
    hours, minutes, seconds = int(parts[0]), int(parts[1]), int(float(parts[2]))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def _items_xml(tag: str, items: tuple[str, ...], indent: str = "      ") -> str:
    if not items:
        return f"    <{tag} />\n"
    lines = [f"    <{tag}>\n"]
    for item in items:
        lines.append(f"{indent}<Item>{item}</Item>\n")
    lines.append(f"    </{tag}>\n")
    return "".join(lines)


def serialize_lesson(lesson: Lesson) -> str:
    """Serialize a :class:`~luzapp.models.lesson.Lesson` to LuzApp XML format.

    The output is a ``<WeekConfig>`` XML string compatible with the ``.luzngl``
    file format consumed by the LuzApp .NET application.

    Args:
        lesson: The lesson to serialize.

    Returns:
        A UTF-8 XML string representing the lesson.
    """
    def whitespace_element(tag: str, value: str) -> str:
        # Preserve whitespace-only text for empty fields (matches LuzApp format)
        if not value.strip():
            return f"    <{tag}>\n    </{tag}>\n"
        return f"    <{tag}>{value}</{tag}>\n"

    start_str = lesson.start_time.strftime(DATE_FORMAT)
    wanted_str = _duration_to_str(lesson.wanted_length)
    actual_str = _duration_to_str(lesson.actual_length)

    lines = [
        "<WeekConfig>\n",
        f'  <LessonInfo lessonId="{lesson.lesson_id}">\n',
        whitespace_element("masterId", lesson.master_id),
        f"    <lessonArray>{lesson.array}</lessonArray>\n",
        f"    <lessonSubject>{lesson.subject}</lessonSubject>\n",
        f"    <lessonStartTime>{start_str}</lessonStartTime>\n",
        f"    <lessonWantedLength>{wanted_str}</lessonWantedLength>\n",
        f"    <lessonActualLength>{actual_str}</lessonActualLength>\n",
        f"    <lessonDisplay>{lesson.display}</lessonDisplay>\n",
        f"    <lessonIsBreak>{lesson.is_break}</lessonIsBreak>\n",
        f"    <lessonIsSkippableForRelevantGroups>{lesson.is_skippable}</lessonIsSkippableForRelevantGroups>\n",
        f"    <lessonIsLocked>{lesson.is_locked}</lessonIsLocked>\n",
        f"    <lessonIsConversationPotential>{lesson.is_conversation_potential}</lessonIsConversationPotential>\n",
        f"    <backgroundColor>{lesson.background_color}</backgroundColor>\n",
        f"    <eventType>{lesson.event_type}</eventType>\n",
        f"    <surpressRoomValidation>{lesson.suppress_room_validation}</surpressRoomValidation>\n",
        whitespace_element("staffComment", lesson.staff_comment),
        whitespace_element("taskType", lesson.task_type),
        whitespace_element("taskParameters", lesson.task_parameters),
        _items_xml("Bizur", lesson.bizur),
        _items_xml("Groups", lesson.groups),
        _items_xml("Tracks", lesson.tracks),
        _items_xml("Classes", lesson.classes),
        "  </LessonInfo>\n",
        "</WeekConfig>",
    ]
    return "".join(lines)


def parse_lesson(source: str | Path) -> Lesson:
    """Parse a :class:`~luzapp.models.lesson.Lesson` from a ``.luzngl`` file or XML string.

    Args:
        source: Either a :class:`~pathlib.Path` to a ``.luzngl`` file or a raw
            XML string.

    Returns:
        A fully populated :class:`~luzapp.models.lesson.Lesson`.

    Raises:
        ValueError: If the XML does not contain a ``<LessonInfo>`` element.
    """
    if isinstance(source, Path):
        tree = ET.parse(source)
        root = tree.getroot()
    else:
        root = ET.fromstring(source)

    info = root.find("LessonInfo")
    if info is None:
        raise ValueError("No LessonInfo element found")

    def text(tag: str) -> str:
        el = info.find(tag)
        return (el.text or "").strip() if el is not None else ""

    def bool_field(tag: str) -> bool:
        return text(tag) == "True"

    def items(tag: str) -> tuple[str, ...]:
        el = info.find(tag)
        if el is None:
            return ()
        return tuple(item.text or "" for item in el.findall("Item"))

    return Lesson(
        lesson_id=int(info.attrib["lessonId"]),
        master_id=text("masterId"),
        array=text("lessonArray"),
        subject=text("lessonSubject"),
        start_time=datetime.strptime(text("lessonStartTime"), DATE_FORMAT),
        wanted_length=_parse_duration(text("lessonWantedLength")),
        actual_length=_parse_duration(text("lessonActualLength")),
        display=text("lessonDisplay"),
        is_break=bool_field("lessonIsBreak"),
        is_skippable=bool_field("lessonIsSkippableForRelevantGroups"),
        is_locked=bool_field("lessonIsLocked"),
        is_conversation_potential=bool_field("lessonIsConversationPotential"),
        background_color=int(text("backgroundColor")),
        event_type=text("eventType"),  # type: ignore[arg-type]
        suppress_room_validation=bool_field("surpressRoomValidation"),
        staff_comment=text("staffComment"),
        task_type=text("taskType"),
        task_parameters=text("taskParameters"),
        bizur=items("Bizur"),
        groups=items("Groups"),
        tracks=items("Tracks"),
        classes=items("Classes"),
    )
