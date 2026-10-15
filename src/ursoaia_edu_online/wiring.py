"""Wokwi wiring diagrams → static SVG.

`wiring/<nume>/diagram.json` (format Wokwi original) este randat de Chromium
headless doar pentru piese (wokwi-elements în shadow DOM); geometria firelor și
compunerea SVG-ului final se fac aici, în Python pur, ca să fie testabile.
"""
from __future__ import annotations

import math
import re

Point = tuple[float, float]

_STEP_RE = re.compile(r"^([hv])(-?\d+(?:\.\d+)?)$")


def _r(v: float) -> float:
    """Rotunjește ca punctele să fie comparabile; -0.0 devine 0.0."""
    v = round(v, 3)
    return v + 0.0


def parse_step(step: str) -> Point:
    m = _STEP_RE.match(step.strip())
    if not m:
        raise ValueError(f"pas de traseu invalid: {step!r}")
    d = float(m.group(2))
    return (d, 0.0) if m.group(1) == "h" else (0.0, d)


def route_points(start: Point, end: Point, steps: list[str]) -> list[Point]:
    if "*" in steps:
        star = steps.index("*")
        head, tail = steps[:star], steps[star + 1:]
    else:
        head, tail = list(steps), []

    x, y = start
    pts: list[Point] = [(x, y)]
    for step in head:
        dx, dy = parse_step(step)
        x, y = x + dx, y + dy
        pts.append((x, y))

    tail_moves = [parse_step(s) for s in tail]
    tx = end[0] - sum(m[0] for m in tail_moves)
    ty = end[1] - sum(m[1] for m in tail_moves)
    pts.append((tx, y))
    pts.append((tx, ty))
    for dx, dy in tail_moves:
        tx, ty = tx + dx, ty + dy
        pts.append((tx, ty))

    out: list[Point] = []
    for px, py in pts:
        p = (_r(px), _r(py))
        if not out or p != out[-1]:
            out.append(p)
    return out


def rotate_point(p: Point, center: Point, degrees: float) -> Point:
    if not degrees:
        return (_r(p[0]), _r(p[1]))
    a = math.radians(degrees)
    dx, dy = p[0] - center[0], p[1] - center[1]
    return (
        _r(center[0] + dx * math.cos(a) - dy * math.sin(a)),
        _r(center[1] + dx * math.sin(a) + dy * math.cos(a)),
    )


def pin_position(part: dict, size: Point, pin_xy: Point) -> Point:
    left, top = float(part.get("left", 0)), float(part.get("top", 0))
    center = (left + size[0] / 2, top + size[1] / 2)
    return rotate_point((left + pin_xy[0], top + pin_xy[1]), center, float(part.get("rotate", 0)))


MARGIN = 16
WIRE_WIDTH = 3
_COLOR_RE = re.compile(r"^#?[A-Za-z0-9]+$")
_ID_RE = re.compile(r'\bid="([^"]+)"')
_SVG_OPEN_RE = re.compile(r"<svg\b([^>]*)>", re.DOTALL)
_SIZE_ATTR_RE = re.compile(r'\s(?:x|y|width|height)="[^"]*"')
_VIEWBOX_RE = re.compile(r'viewBox="\s*(-?[\d.]+)[\s,]+(-?[\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"')
_RULE_RE = re.compile(r"([^{}]+)\{((?:[^{}]|\{[^{}]*\})*)\}")


def _n(v: float) -> str:
    """Număr compact pentru SVG: 12.0 → '12', 12.345678 → '12.346'."""
    return f"{_r(v):g}"


def _safe_id(raw: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]", "-", raw)


def prefix_ids(markup: str, prefix: str) -> str:
    ids = set(_ID_RE.findall(markup))
    if not ids:
        return markup
    alt = "|".join(re.escape(i) for i in sorted(ids, key=len, reverse=True))
    markup = re.sub(rf'\bid="({alt})"', lambda m: f'id="{prefix}-{m.group(1)}"', markup)
    markup = re.sub(rf"url\(#({alt})\)", lambda m: f"url(#{prefix}-{m.group(1)})", markup)
    markup = re.sub(rf'href="#({alt})"', lambda m: f'href="#{prefix}-{m.group(1)}"', markup)
    return markup


def scope_css(css: str, scope: str) -> str:
    out: list[str] = []
    for m in _RULE_RE.finditer(css):
        selector, body = m.group(1).strip(), m.group(2)
        if selector.startswith("@"):
            if selector.startswith(("@media", "@supports")):
                out.append(f"{selector}{{{scope_css(body, scope)}}}")
            else:
                out.append(f"{selector}{{{body}}}")
            continue
        scoped = []
        for sel in selector.split(","):
            sel = sel.strip()
            if sel.startswith(":host"):
                sel = re.sub(r":host\(([^)]*)\)", rf"#{scope}\1", sel).replace(":host", f"#{scope}")
            else:
                sel = f"#{scope} {sel}"
            scoped.append(sel)
        out.append(f"{', '.join(scoped)}{{{body}}}")
    return "\n".join(out)


def place_svg(markup: str, x: float, y: float, w: float, h: float) -> str:
    m = _SVG_OPEN_RE.search(markup)
    if not m:
        raise ValueError("piesa nu a produs un <svg>")
    attrs = _SIZE_ATTR_RE.sub("", m.group(1))
    if "viewBox" not in attrs:
        attrs += f' viewBox="0 0 {_n(w)} {_n(h)}"'
    new_open = f'<svg x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}"{attrs}>'
    return markup[: m.start()] + new_open + markup[m.end():]


def _pin(diagram: dict, rendered: dict[str, dict], ref: str) -> Point:
    part_id, _, pin_name = ref.partition(":")
    part = next((p for p in diagram["parts"] if p["id"] == part_id), None)
    if part is None or part_id not in rendered:
        raise ValueError(f"piesă necunoscută în conexiunea {ref}")
    info = rendered[part_id]
    if pin_name not in info["pins"]:
        raise ValueError(f"pin necunoscut în conexiunea {ref}")
    px, py = info["pins"][pin_name]
    return pin_position(part, (info["width"], info["height"]), (px, py))


def compose_svg(diagram: dict, rendered: dict[str, dict]) -> str:
    extent: list[Point] = []
    parts_markup: list[str] = []
    styles: list[str] = []

    for part in diagram["parts"]:
        pid = part["id"]
        info = rendered[pid]
        scope = f"p-{_safe_id(pid)}"
        x, y = float(part.get("left", 0)), float(part.get("top", 0))
        w, h = float(info["width"]), float(info["height"])
        rot = float(part.get("rotate", 0))
        cx, cy = x + w / 2, y + h / 2
        inner = place_svg(prefix_ids(info["svg"], scope), x, y, w, h)
        transform = f' transform="rotate({_n(rot)} {_n(cx)} {_n(cy)})"' if rot else ""
        parts_markup.append(f'<g id="{scope}"{transform}>{inner}</g>')
        if info.get("css"):
            styles.append(scope_css(info["css"], scope))
        for corner in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
            extent.append(rotate_point(corner, (cx, cy), rot))

    wires: list[str] = []
    for conn in diagram.get("connections", []):
        src, dst, color = conn[0], conn[1], conn[2]
        steps = conn[3] if len(conn) > 3 else []
        if not _COLOR_RE.match(color):
            raise ValueError(f"culoare invalidă în conexiunea {src} → {dst}: {color!r}")
        pts = route_points(_pin(diagram, rendered, src), _pin(diagram, rendered, dst), steps)
        extent.extend(pts)
        d = " ".join(f"{'M' if i == 0 else 'L'}{_n(px)} {_n(py)}" for i, (px, py) in enumerate(pts))
        common = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
        wires.append(f'<path d="{d}" {common} stroke="#ffffff" stroke-opacity="0.9" stroke-width="{WIRE_WIDTH + 2}"/>')
        wires.append(f'<path d="{d}" {common} stroke="{color}" stroke-width="{WIRE_WIDTH}"/>')
        for px, py in (pts[0], pts[-1]):
            wires.append(f'<circle cx="{_n(px)}" cy="{_n(py)}" r="2.6" fill="{color}"/>')

    minx = min(p[0] for p in extent) - MARGIN
    miny = min(p[1] for p in extent) - MARGIN
    maxx = max(p[0] for p in extent) + MARGIN
    maxy = max(p[1] for p in extent) + MARGIN
    w, h = maxx - minx, maxy - miny
    style = f"<style>{''.join(styles)}</style>" if styles else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="{_n(minx)} {_n(miny)} {_n(w)} {_n(h)}" width="{_n(w)}" height="{_n(h)}">'
        f"{style}"
        f'<rect x="{_n(minx)}" y="{_n(miny)}" width="{_n(w)}" height="{_n(h)}" fill="#ffffff"/>'
        f"{''.join(parts_markup)}{''.join(wires)}</svg>\n"
    )


def svg_size(svg_text: str) -> tuple[int, int]:
    m = _VIEWBOX_RE.search(svg_text)
    if not m:
        raise ValueError("SVG fără viewBox")
    return round(float(m.group(3))), round(float(m.group(4)))
