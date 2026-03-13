from pathlib import Path

from luzapp.models.school import SchoolConfig
from luzapp.serializers.school_serializer import serialize_school


def save_school(config_path: Path, config: SchoolConfig) -> None:
    """Serialize and overwrite the school config file.

    Args:
        config_path: Path to the ``config.school`` file to write.
        config: The :class:`~luzapp.models.school.SchoolConfig` to persist.
    """
    xml_str = serialize_school(config)
    config_path.write_text(xml_str, encoding="utf-8")
