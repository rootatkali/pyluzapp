from pydantic import BaseModel, ConfigDict


class NamedColor(BaseModel):
    """An RGB colour with an optional display name, stored in ``config.school``.

    Colours are exchanged with LuzApp as .NET ARGB signed integers (alpha is
    always ``0xFF``).

    Args:
        name: Display name of the colour (e.g. ``"Red"``).
        r: Red channel, 0–255.
        g: Green channel, 0–255.
        b: Blue channel, 0–255.
    """

    model_config = ConfigDict(frozen=True)

    name: str
    r: int
    g: int
    b: int

    def to_argb_int(self) -> int:
        """Return the colour as a .NET ARGB signed 32-bit integer (alpha = 255)."""
        unsigned = (0xFF << 24) | (self.r << 16) | (self.g << 8) | self.b
        if unsigned >= 2**31:
            return unsigned - 2**32
        return unsigned

    @classmethod
    def from_argb_int(cls, argb_int: int, name: str = "") -> "NamedColor":
        """Construct a :class:`NamedColor` from a .NET ARGB signed integer.

        Args:
            argb_int: Signed 32-bit ARGB value (alpha channel is ignored).
            name: Optional display name for the resulting colour.
        """
        unsigned = argb_int & 0xFFFFFFFF
        r = (unsigned >> 16) & 0xFF
        g = (unsigned >> 8) & 0xFF
        b = unsigned & 0xFF
        return cls(name=name, r=r, g=g, b=b)
