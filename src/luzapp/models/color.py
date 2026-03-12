from pydantic import BaseModel, ConfigDict


class NamedColor(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    r: int
    g: int
    b: int

    def to_argb_int(self) -> int:
        unsigned = (0xFF << 24) | (self.r << 16) | (self.g << 8) | self.b
        if unsigned >= 2**31:
            return unsigned - 2**32
        return unsigned

    @classmethod
    def from_argb_int(cls, argb_int: int, name: str = "") -> "NamedColor":
        unsigned = argb_int & 0xFFFFFFFF
        r = (unsigned >> 16) & 0xFF
        g = (unsigned >> 8) & 0xFF
        b = unsigned & 0xFF
        return cls(name=name, r=r, g=g, b=b)
