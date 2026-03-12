import pytest
from luzapp.models.color import NamedColor


def test_white_to_argb():
    color = NamedColor(name="white", r=255, g=255, b=255)
    assert color.to_argb_int() == -1


def test_red_to_argb():
    color = NamedColor(name="red", r=255, g=0, b=0)
    # 0xFF << 24 | 0xFF << 16 = 0xFFFF0000 = 4294901760 -> signed = 4294901760 - 2**32 = -65536
    assert color.to_argb_int() == -65536


def test_black_to_argb():
    color = NamedColor(name="black", r=0, g=0, b=0)
    # 0xFF000000 = 4278190080 -> signed = 4278190080 - 2**32 = -16777216
    assert color.to_argb_int() == -16777216


def test_from_argb_minus_one():
    color = NamedColor.from_argb_int(-1)
    assert color.r == 255
    assert color.g == 255
    assert color.b == 255


def test_from_argb_specific():
    # -9728477 -> unsigned = 4285238819 -> hex 0xFF6B8E23 -> R=107, G=142, B=35
    color = NamedColor.from_argb_int(-9728477)
    assert color.r == 107
    assert color.g == 142
    assert color.b == 35


def test_round_trip():
    original = NamedColor(name="test", r=100, g=150, b=200)
    argb = original.to_argb_int()
    recovered = NamedColor.from_argb_int(argb, name="test")
    assert recovered.r == original.r
    assert recovered.g == original.g
    assert recovered.b == original.b


def test_frozen_model():
    color = NamedColor(name="red", r=255, g=0, b=0)
    with pytest.raises(Exception):
        color.r = 100  # type: ignore
