from datetime import time, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
from luzapp.models.school import SchoolConfig, Group, Track, ClassRoom, StaffGroup, Person
from luzapp.models.color import NamedColor


def parse_school(source: str | Path) -> SchoolConfig:
    if isinstance(source, Path):
        root = ET.parse(source).getroot()
    else:
        root = ET.fromstring(source)

    name = root.attrib.get("name", "")
    sync_server = root.attrib.get("sync-server", "")

    elements = root.find("elements")

    if elements is not None:
        groups_el = elements.find("groups")
        groups = tuple(
            Group(name=g.attrib["name"], size=int(g.attrib.get("size", 0)))
            for g in (list(groups_el) if groups_el is not None else [])
            if g.tag == "group"
        )
        tracks_el = elements.find("tracks")
        tracks = tuple(
            Track(name=t.attrib["name"])
            for t in (list(tracks_el) if tracks_el is not None else [])
            if t.tag == "track"
        )
        classes_el = elements.find("classes")
        classes = tuple(
            ClassRoom(
                name=c.attrib["name"],
                seats=int(c.attrib.get("seats", 0)),
                workstations=int(c.attrib.get("workstations", 0)),
            )
            for c in (list(classes_el) if classes_el is not None else [])
            if c.tag == "class"
        )
    else:
        groups: tuple[Group, ...] = ()
        tracks: tuple[Track, ...] = ()
        classes: tuple[ClassRoom, ...] = ()

    default_class_el = root.find("defaultclass")
    default_class = default_class_el.attrib.get("name", "") if default_class_el is not None else ""

    segel_el = root.find("segel")
    staff_groups: tuple[StaffGroup, ...] = ()
    if segel_el is not None:
        staff_groups = tuple(
            StaffGroup(
                name=sg.attrib["name"],
                members=tuple(
                    Person(name=p.attrib["name"], sex=p.attrib.get("sex", ""))
                    for p in sg.findall("person")
                ),
            )
            for sg in segel_el.findall("group")
        )

    week_el = root.find("week")
    week_days = int(week_el.attrib.get("days", 7)) if week_el is not None else 7

    day_el = root.find("day")
    if day_el is not None:
        start_parts = day_el.attrib["start"].split(":")
        day_start = time(int(start_parts[0]), int(start_parts[1]))
        length_parts = day_el.attrib["length"].split(":")
        day_length = timedelta(hours=int(length_parts[0]), minutes=int(length_parts[1]))
    else:
        day_start = time(8, 0)
        day_length = timedelta(hours=12)

    hours_el = root.find("hours")
    time_grid: tuple[time, ...] = ()
    if hours_el is not None:
        time_grid = tuple(
            time(*map(int, line.attrib["time"].split(":")))
            for line in hours_el.findall("line")
        )

    colors_el = root.find("colors")
    colors: tuple[NamedColor, ...] = ()
    if colors_el is not None:
        colors = tuple(
            NamedColor(
                name=c.attrib["name"],
                r=int(c.attrib["R"]),
                g=int(c.attrib["G"]),
                b=int(c.attrib["B"]),
            )
            for c in colors_el.findall("color")
        )

    return SchoolConfig(
        name=name,
        sync_server=sync_server,
        groups=groups,
        tracks=tracks,
        classes=classes,
        staff_groups=staff_groups,
        default_class=default_class,
        week_days=week_days,
        day_start=day_start,
        day_length=day_length,
        time_grid=time_grid,
        colors=colors,
    )
