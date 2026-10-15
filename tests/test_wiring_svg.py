import re

import pytest

from ursoaia_edu_online.wiring import compose_svg, place_svg, prefix_ids, scope_css, svg_size

LED_SVG = '<svg width="5mm" height="11mm" viewBox="0 0 5 11"><defs><radialGradient id="glow"/></defs><circle fill="url(#glow)"/><use href="#glow"/></svg>'


def fake(width, height, pins, svg=LED_SVG, css=""):
    return {"width": width, "height": height, "svg": svg, "css": css, "pins": pins}


def test_prefix_ids_rewrites_ids_and_references():
    out = prefix_ids(LED_SVG, "p-led1")
    assert 'id="p-led1-glow"' in out
    assert "url(#p-led1-glow)" in out
    assert 'href="#p-led1-glow"' in out
    assert 'id="glow"' not in out


def test_scope_css_host_and_descendants():
    css = ":host { display: inline-block; }\n.body, text { fill: red; }"
    out = scope_css(css, "p-uno")
    assert "#p-uno{" in out.replace(" ", "")
    assert "#p-uno .body" in out and "#p-uno text" in out


def test_scope_css_keeps_keyframes_unscoped():
    out = scope_css("@keyframes blink { 0% { opacity: 0; } 100% { opacity: 1; } }", "p-x")
    assert out.startswith("@keyframes blink")
    assert "#p-x" not in out


def test_place_svg_replaces_size_and_position():
    out = place_svg(LED_SVG, 10, 20, 19, 42)
    head = out[: out.index(">") + 1]
    assert 'x="10"' in head and 'y="20"' in head and 'width="19"' in head and 'height="42"' in head
    assert "5mm" not in head
    assert 'viewBox="0 0 5 11"' in head


def _diagram(**over):
    d = {
        "parts": [
            {"type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0},
            {"type": "wokwi-led", "id": "led1", "top": -100, "left": 300},
        ],
        "connections": [["uno:13", "led1:A", "green", ["v-50"]]],
    }
    d.update(over)
    return d


RENDERED = {
    "uno": fake(274, 202, {"13": [129, 9]}, svg='<svg width="72mm" viewBox="0 0 72 53"></svg>'),
    "led1": fake(19, 42, {"A": [12, 42], "C": [7, 42]}),
}


def test_compose_svg_has_parts_wires_and_viewbox_covering_everything():
    out = compose_svg(_diagram(), RENDERED)
    assert out.startswith("<svg ")
    assert '<g id="p-uno"' in out and '<g id="p-led1"' in out
    assert 'stroke="green"' in out
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', out).group(1).split()]
    minx, miny, w, h = vb
    assert minx <= -16 + 0.01 and miny <= -100 - 16 + 0.01
    assert minx + w >= 319 + 16 - 0.01 and miny + h >= 202 + 16 - 0.01


def test_compose_svg_two_parts_same_type_have_distinct_ids():
    d = _diagram(parts=[
        {"type": "wokwi-led", "id": "led1", "top": 0, "left": 0},
        {"type": "wokwi-led", "id": "led2", "top": 0, "left": 50},
    ], connections=[])
    out = compose_svg(d, {"led1": fake(19, 42, {}), "led2": fake(19, 42, {})})
    ids = re.findall(r'\bid="([^"]+)"', out)
    assert len(ids) == len(set(ids))


def test_compose_svg_rotated_part_transform_and_pin():
    d = _diagram(parts=[
        {"type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0},
        {"type": "wokwi-led", "id": "led1", "top": -100, "left": 300, "rotate": 90},
    ])
    out = compose_svg(d, RENDERED)
    assert 'transform="rotate(90 309.5 -79)"' in out
    # pinul A (12,42) al LED-ului rotit: centrul (309.5,-79) → (288.5,-76.5)
    assert "288.5 -76.5" in out


def test_compose_svg_unknown_pin_names_the_reference():
    d = _diagram(connections=[["uno:99", "led1:A", "green", []]])
    with pytest.raises(ValueError, match="uno:99"):
        compose_svg(d, RENDERED)


def test_compose_svg_unknown_part_names_the_reference():
    d = _diagram(connections=[["nano:13", "led1:A", "green", []]])
    with pytest.raises(ValueError, match="nano:13"):
        compose_svg(d, RENDERED)


def test_compose_svg_rejects_color_injection():
    d = _diagram(connections=[["uno:13", "led1:A", 'red" onload="x', []]])
    with pytest.raises(ValueError, match="culoare"):
        compose_svg(d, RENDERED)


def test_svg_size_reads_viewbox():
    assert svg_size('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -116 351.2 334.4">') == (351, 334)


def test_compose_svg_drops_comments_for_deterministic_output():
    # Lit lasă <!--?lit$<număr aleator>$--> în shadow DOM: fiecare randare ar da alt fișier
    svg = '<svg viewBox="0 0 5 11"><!--?lit$123456$--><g/><!----></svg>'
    d = _diagram(parts=[{"type": "wokwi-led", "id": "led1", "top": 0, "left": 0}], connections=[])
    out = compose_svg(d, {"led1": fake(19, 42, {}, svg=svg)})
    assert "<!--" not in out


def test_compose_svg_embeds_source_hash():
    d = _diagram(parts=[{"type": "wokwi-led", "id": "led1", "top": 0, "left": 0}], connections=[])
    out = compose_svg(d, {"led1": fake(19, 42, {})}, source_hash="abc123")
    assert out.startswith("<svg ") and 'data-source-hash="abc123"' in out[: out.index(">")]
