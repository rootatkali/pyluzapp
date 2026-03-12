from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
from luzapp.models.week import WeekConfig

WEEK_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"


def parse_week(source: str | Path) -> WeekConfig:
    if isinstance(source, Path):
        root = ET.parse(source).getroot()
    else:
        root = ET.fromstring(source)

    def items(tag: str) -> tuple[str, ...]:
        el = root.find(tag)
        if el is None:
            return ()
        return tuple(item.text or "" for item in el.findall("Item"))

    return WeekConfig(
        number=int(root.attrib["number"]),
        days_in_week=int(root.attrib["daysInWeek"]),
        start_time=datetime.strptime(root.attrib["startTime"], WEEK_DATE_FORMAT),
        groups=items("Groups"),
        tracks=items("Tracks"),
        classes=items("Classes"),
    )


def serialize_week(week: WeekConfig) -> str:
    start_str = week.start_time.strftime(WEEK_DATE_FORMAT)

    def items_xml(tag: str, items: tuple[str, ...]) -> str:
        lines = [f"  <{tag}>\n"]
        for item in items:
            lines.append(f"    <Item>{item}</Item>\n")
        lines.append(f"  </{tag}>\n")
        return "".join(lines)

    lines = [
        f'<WeekConfig number="{week.number}" daysInWeek="{week.days_in_week}" startTime="{start_str}">\n',
        items_xml("Groups", week.groups),
        items_xml("Tracks", week.tracks),
        items_xml("Classes", week.classes),
        "</WeekConfig>",
    ]
    return "".join(lines)
