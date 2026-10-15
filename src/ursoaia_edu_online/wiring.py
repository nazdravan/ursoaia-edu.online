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
