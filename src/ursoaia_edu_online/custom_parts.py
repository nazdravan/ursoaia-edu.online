"""Piese desenate local, pentru componente din kit pe care @wokwi/elements nu le are.

`wokwi-74hc595` și `wokwi-relay-module` sunt piese native pe wokwi.com (dar nu în
biblioteca @wokwi/elements); le desenăm aici cu aceleași nume de pini, ca
diagram.json să rămână compatibil. Tipurile `ursoaia-*` există doar pe site.

Fiecare piesă întoarce același format ca `wiring_render.js`:
`{"width", "height", "svg", "css", "pins": {nume: [x, y]}}`, pinii pe marginea piesei.
"""
from __future__ import annotations

from typing import Callable

PITCH = 9.6  # 0.1" la scara Wokwi
FONT = 'font-family="sans-serif"'


def _svg(w: float, h: float, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" viewBox="0 0 {w:g} {h:g}">{body}</svg>'


def _text(x: float, y: float, s: str, size: float = 5, fill: str = "#ffffff", anchor: str = "middle", extra: str = "") -> str:
    return f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}" text-anchor="{anchor}" {FONT}{extra}>{s}</text>'


def _label(name: str) -> str:
    """GND.2 → GND: sufixul face doar numele de pin unic."""
    return name.split(".")[0].replace("-", "−")


def _part(w: float, h: float, body: str, pins: dict[str, tuple[float, float]]) -> dict:
    return {"width": w, "height": h, "svg": _svg(w, h, body), "css": "",
            "pins": {k: [round(x, 2), round(y, 2)] for k, (x, y) in pins.items()}}


def _dip(title: str, top: list[str], bottom: list[str]) -> dict:
    """Cip DIP orizontal: pinul 1 jos-stânga, numerotare în sens invers acelor de ceasornic."""
    n = len(bottom)
    margin, leg, body_h = 6.0, 6.0, 36.0
    w, h = n * PITCH + 2 * margin, body_h + 2 * leg
    xs = [margin + PITCH / 2 + i * PITCH for i in range(n)]
    parts = [f'<rect x="0" y="{leg:g}" width="{w:g}" height="{body_h:g}" rx="2" fill="#262626"/>',
             f'<path d="M0 {h / 2 - 5:g} a5 5 0 0 1 0 10z" fill="#111111"/>',
             f'<circle cx="{margin + 3:g}" cy="{h - leg - 5:g}" r="1.6" fill="#555555"/>',
             _text(w / 2, h / 2 + 2.5, title, 7, "#d4d4d4")]
    pins: dict[str, tuple[float, float]] = {}
    for x, name in zip(xs, top):
        parts.append(f'<rect x="{x - 1.5:g}" y="0" width="3" height="{leg + 1:g}" fill="#b5b5b5"/>')
        parts.append(_text(x, leg + 6, _label(name), 3.4, "#e5e5e5"))
        pins[name] = (x, 0)
    for x, name in zip(xs, bottom):
        parts.append(f'<rect x="{x - 1.5:g}" y="{h - leg - 1:g}" width="3" height="{leg + 1:g}" fill="#b5b5b5"/>')
        parts.append(_text(x, h - leg - 2.5, _label(name), 3.4, "#e5e5e5"))
        pins[name] = (x, h)
    return _part(w, h, "".join(parts), pins)


def _header(x: float, ys: list[float], names: list[str], label_dx: float) -> tuple[str, dict]:
    """Pini tată pe marginea stângă (label_dx > 0) sau dreaptă (label_dx < 0) a unui modul."""
    parts, pins = [], {}
    anchor = "start" if label_dx > 0 else "end"
    for y, name in zip(ys, names):
        x2 = x + (8 if label_dx > 0 else -8)
        parts.append(f'<line x1="{x:g}" y1="{y:g}" x2="{x2:g}" y2="{y:g}" stroke="#c9a227" stroke-width="2"/>')
        parts.append(f'<rect x="{min(x, x2) + (5 if label_dx > 0 else 0):g}" y="{y - 3.5:g}" width="3" height="7" fill="#1a1a1a"/>')
        parts.append(_text(x2 + label_dx, y + 1.8, _label(name), 5, "#ffffff", anchor))
        pins[name] = (x, y)
    return "".join(parts), pins


def relay_module(attrs: dict) -> dict:
    w, h = 120.0, 60.0
    body = [f'<rect x="8" y="2" width="{w - 16:g}" height="{h - 4:g}" rx="3" fill="#1f5fa8"/>',
            '<rect x="38" y="10" width="44" height="38" rx="2" fill="#2b7bd6" stroke="#174a85"/>',
            _text(60, 27, "SRD-05VDC", 5), _text(60, 35, "SL-C", 4.5),
            '<circle cx="28" cy="50" r="2.4" fill="#e03131"/>',
            f'<rect x="{w - 30:g}" y="8" width="22" height="44" rx="2" fill="#0b4fa0"/>']
    left, lp = _header(0, [18, 30, 42], ["VCC", "GND", "IN"], 3)
    right, rp = _header(w, [18, 30, 42], ["NO", "COM", "NC"], -3)
    return _part(w, h, "".join(body) + left + right, {**lp, **rp})


def shift_register(attrs: dict) -> dict:
    return _dip("74HC595",
                top=["VCC", "Q0", "DS", "OE", "STCP", "SHCP", "MR", "Q7S"],
                bottom=["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "GND"])


def l293d(attrs: dict) -> dict:
    return _dip("L293D",
                top=["VSS", "IN4", "OUT4", "GND.4", "GND.3", "OUT3", "IN3", "EN2"],
                bottom=["EN1", "IN1", "OUT1", "GND.1", "GND.2", "OUT2", "IN2", "VS"])


def uln2003_board(attrs: dict) -> dict:
    w, h = 110.0, 96.0
    body = [f'<rect x="8" y="8" width="{w - 16:g}" height="{h - 16:g}" rx="3" fill="#1e7a3c"/>',
            '<rect x="36" y="0" width="40" height="14" rx="1.5" fill="#f2f2f2" stroke="#bdbdbd"/>',
            _text(56, 10, "MOTOR", 5, "#555555"),
            '<rect x="40" y="34" width="34" height="20" rx="1.5" fill="#262626"/>',
            _text(57, 46.5, "ULN2003", 5.5, "#d4d4d4")]
    for i, x in enumerate([42, 50, 58, 66]):
        body.append(f'<circle cx="{x}" cy="66" r="2.6" fill="#e03131"/>')
        body.append(_text(x, 75, "ABCD"[i], 4))
    left, lp = _header(0, [26, 36, 46, 56], ["IN1", "IN2", "IN3", "IN4"], 3)
    pins = {**lp, "MOTOR": (56, 0)}
    for x, name, sign in [(88, "VCC", "+"), (98, "GND", "−")]:
        body.append(f'<line x1="{x}" y1="{h - 8:g}" x2="{x}" y2="{h:g}" stroke="#c9a227" stroke-width="2"/>')
        body.append(_text(x, h - 12, sign, 6))
        pins[name] = (x, h)
    return _part(w, h, "".join(body) + left, pins)


def stepper_28byj48(attrs: dict) -> dict:
    w, h = 112.0, 150.0
    colors = ["#1c7ed6", "#f783ac", "#fcc419", "#fd7e14", "#e03131"]
    body = [f'<path d="M{50 + i * 3} 104 L{50 + i * 3} {h - 8:g}" stroke="{c}" stroke-width="2.2"/>'
            for i, c in enumerate(colors)]
    body += [f'<rect x="46" y="{h - 9:g}" width="20" height="9" rx="1" fill="#f2f2f2" stroke="#bdbdbd"/>',
             '<rect x="6" y="36" width="100" height="20" rx="3" fill="#c9ccd1"/>',
             '<circle cx="56" cy="56" r="46" fill="#d7dade" stroke="#9aa0a6"/>',
             '<circle cx="56" cy="56" r="34" fill="#2f6fc0"/>',
             '<circle cx="56" cy="40" r="8" fill="#e9ecef"/>',
             '<rect x="53.5" y="34" width="5" height="12" fill="#9aa0a6"/>',
             _text(56, 78, "28BYJ-48", 7)]
    return _part(w, h, "".join(body), {"MOTOR": (56, h)})


def dc_motor(attrs: dict) -> dict:
    w, h = 110.0, 60.0
    body = ['<rect x="22" y="8" width="70" height="44" rx="8" fill="#b8bec6" stroke="#8a9099"/>',
            '<rect x="16" y="14" width="10" height="32" rx="3" fill="#8a9099"/>',
            '<rect x="92" y="26" width="18" height="8" rx="2" fill="#adb5bd"/>',
            _text(57, 34, "M", 14, "#495057")]
    pins = {}
    for y, name, sign in [(22, "1", "+"), (38, "2", "−")]:
        body.append(f'<rect x="0" y="{y - 2.5:g}" width="18" height="5" fill="#c9a227"/>')
        body.append(_text(9, y - 4, sign, 6, "#495057"))
        pins[name] = (0, y)
    return _part(w, h, "".join(body), pins)


def water_level_sensor(attrs: dict) -> dict:
    w, h = 46.0, 150.0
    body = [f'<rect x="2" y="8" width="{w - 4:g}" height="{h - 8:g}" rx="2" fill="#c92a2a"/>',
            _text(23, 30, "WATER", 5.5), _text(23, 37, "SENSOR", 5.5)]
    for i in range(10):
        x = 8 + i * 3.3
        y1 = 50 if i % 2 == 0 else 56
        body.append(f'<line x1="{x:g}" y1="{y1}" x2="{x:g}" y2="{h - 6:g}" stroke="#ced4da" stroke-width="1.6"/>')
    pins = {}
    for x, name, sign in [(13.4, "S", "S"), (23, "VCC", "+"), (32.6, "GND", "−")]:
        body.append(f'<line x1="{x:g}" y1="0" x2="{x:g}" y2="10" stroke="#c9a227" stroke-width="2"/>')
        body.append(_text(x, 18, sign, 6))
        pins[name] = (x, 0)
    return _part(w, h, "".join(body), pins)


def _two_leg(drawing: str, h: float = 64.0, w: float = 26.0) -> dict:
    x1, x2 = w / 2 - PITCH / 2, w / 2 + PITCH / 2
    legs = (f'<line x1="{x1:g}" y1="18" x2="{x1:g}" y2="{h:g}" stroke="#adb5bd" stroke-width="1.6"/>'
            f'<line x1="{x2:g}" y1="18" x2="{x2:g}" y2="{h:g}" stroke="#adb5bd" stroke-width="1.6"/>')
    return _part(w, h, legs + drawing, {"1": (x1, h), "2": (x2, h)})


def thermistor(attrs: dict) -> dict:
    return _two_leg('<ellipse cx="13" cy="13" rx="8" ry="10" fill="#343a40"/>' + _text(13, 15, "NTC", 4.5))


def photoresistor(attrs: dict) -> dict:
    zig = "M6 9 h14 v3 h-14 v3 h14 v3 h-14"
    return _two_leg('<circle cx="13" cy="13" r="11" fill="#e8c39e" stroke="#c08b5c"/>'
                    f'<path d="{zig}" fill="none" stroke="#c0392b" stroke-width="1.6"/>')


def tilt_switch(attrs: dict) -> dict:
    return _two_leg('<rect x="5" y="0" width="16" height="22" rx="4" fill="#343a40"/>'
                    '<rect x="5" y="0" width="16" height="5" rx="2" fill="#c9a227"/>')


def battery_9v(attrs: dict) -> dict:
    w, h = 60.0, 104.0
    body = [f'<rect x="2" y="12" width="{w - 4:g}" height="{h - 12:g}" rx="4" fill="#212529"/>',
            f'<rect x="2" y="12" width="{w - 4:g}" height="34" rx="4" fill="#f08c00"/>',
            _text(30, 36, "9V", 14), _text(30, 80, "BATTERY", 6.5, "#adb5bd")]
    pins = {}
    for x, name, shape in [(18, "+", "circle"), (42, "-", "hex")]:
        if shape == "circle":
            body.append(f'<rect x="{x - 5}" y="4" width="10" height="9" rx="4" fill="#ced4da"/>')
        else:
            body.append(f'<path d="M{x - 6} 13 l2 -9 h8 l2 9z" fill="#ced4da"/>')
        body.append(f'<line x1="{x}" y1="0" x2="{x}" y2="4" stroke="#ced4da" stroke-width="2"/>')
        body.append(_text(x, 24, "+" if name == "+" else "−", 9, "#212529"))
        pins[name] = (x, 0)
    return _part(w, h, "".join(body), pins)


CUSTOM_PARTS: dict[str, Callable[[dict], dict]] = {
    "wokwi-74hc595": shift_register,
    "wokwi-relay-module": relay_module,
    "ursoaia-l293d": l293d,
    "ursoaia-uln2003": uln2003_board,
    "ursoaia-28byj48": stepper_28byj48,
    "ursoaia-dc-motor": dc_motor,
    "ursoaia-water-level-sensor": water_level_sensor,
    "ursoaia-thermistor": thermistor,
    "ursoaia-photoresistor": photoresistor,
    "ursoaia-tilt-switch": tilt_switch,
    "ursoaia-battery-9v": battery_9v,
}


def render_custom(part_type: str, attrs: dict) -> dict:
    return CUSTOM_PARTS[part_type](attrs)
