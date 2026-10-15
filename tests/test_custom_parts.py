import xml.etree.ElementTree as ET

import pytest

from ursoaia_edu_online.custom_parts import CUSTOM_PARTS, render_custom
from ursoaia_edu_online.wiring import compose_svg


@pytest.mark.parametrize("part_type", sorted(CUSTOM_PARTS))
def test_custom_part_is_well_formed_with_pins_on_its_edge(part_type):
    info = render_custom(part_type, {})
    assert info["width"] > 0 and info["height"] > 0
    ET.fromstring(info["svg"])
    assert info["pins"]
    for name, (x, y) in info["pins"].items():
        assert -0.01 <= x <= info["width"] + 0.01, name
        assert -0.01 <= y <= info["height"] + 0.01, name


def test_74hc595_uses_wokwi_pin_names():
    pins = render_custom("wokwi-74hc595", {})["pins"]
    assert set(pins) == {"Q0", "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q7S",
                         "DS", "STCP", "SHCP", "MR", "OE", "VCC", "GND"}


def test_relay_module_uses_wokwi_pin_names():
    assert set(render_custom("wokwi-relay-module", {})["pins"]) == {"VCC", "GND", "IN", "NO", "COM", "NC"}


def test_l293d_pins_follow_datasheet_numbering():
    pins = render_custom("ursoaia-l293d", {})["pins"]
    # pinul 1 (EN1) jos-stânga, pinul 16 (VSS) sus-stânga, ca la orice DIP
    assert pins["EN1"][1] > pins["VSS"][1]
    assert pins["EN1"][0] == pytest.approx(pins["VSS"][0])
    assert pins["VS"][0] > pins["EN1"][0]


def test_unknown_custom_type_is_rejected():
    with pytest.raises(KeyError):
        render_custom("ursoaia-nope", {})


def test_custom_parts_compose_with_wires():
    diagram = {
        "parts": [
            {"type": "wokwi-74hc595", "id": "sr", "top": 0, "left": 0},
            {"type": "ursoaia-battery-9v", "id": "bat", "top": 0, "left": 200},
        ],
        "connections": [["bat:+", "sr:VCC", "red", []]],
    }
    rendered = {p["id"]: render_custom(p["type"], {}) for p in diagram["parts"]}
    out = compose_svg(diagram, rendered)
    ET.fromstring(out)
    assert 'stroke="red"' in out
