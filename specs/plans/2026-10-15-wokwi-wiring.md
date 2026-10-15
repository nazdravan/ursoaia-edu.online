# Scheme de conectare Wokwi — plan de implementare

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fiecare pagină de proiect primește o schemă de montaj Wokwi, generată la build din `wiring/<nume>/diagram.json` ca SVG static. Pilotul acoperă 3 pagini.

**Architecture:** Partea de geometrie și compunere SVG e în Python pur, în `src/ursoaia_edu_online/wiring.py`, testată cu pytest. Chromium headless (Playwright) face un singur lucru: instanțiază piesele `@wokwi/elements` și întoarce markup-ul lor SVG, CSS-ul din shadow root, dimensiunile și coordonatele pinilor (`wiring_render.js`). Hook-ul MkDocs `hooks/wokwi.py` înlocuiește markerul `[[wokwi:<nume>|<id>]]` cu o figură HTML. SVG-urile generate se commit-uiesc, deci CI-ul nu are nevoie de Chromium.

**Tech Stack:** Python 3.12, uv, MkDocs 1.6.1 + mkdocs-static-i18n 1.3.1, Playwright (Python, Chromium), `@wokwi/elements@1.9.1` (UMD bundle), pytest, Tailwind v3 (`tailwind/input.css`).

**Spec:** `specs/2026-10-15-wokwi-wiring-design.md`

## Global Constraints

- Branch: `wokwi-wiring`. Commit-urile urmează stilul repo-ului (`feat(wiring): …`, `content(…): …`, `docs: …`), fără atribuire Claude sau trailer de sesiune.
- `diagram.json` = format Wokwi original, fără câmpuri proprii. Câmpurile citite: `parts[].type/id/top/left/rotate/attrs`, `connections[] = [from, to, culoare, traseu]`.
- Sursa e în `wiring/<nume>/` (rădăcina repo-ului). Ieșirea e în `docs/assets/images/wiring/<nume>.svg`, commit-uită.
- Bundle: `@wokwi/elements@1.9.1` de la `https://unpkg.com/@wokwi/elements@1.9.1/dist/wokwi-elements.bundle.js`, descărcat în `tools/wokwi/` (gitignored).
- Pe site nu se încarcă JS și nici resurse de pe CDN. SVG-ul e servit ca `<img>`.
- `URSOAIA_SKIP_DIAGRAMS=1` sare pasul. Fără Playwright sau fără Chromium: avertisment, iar build-ul continuă.
- Textele figurii: RO „Schema de conectare” / „Simulează în Wokwi”, EN „Wiring diagram” / „Simulate in Wokwi”.
- Trasee: pașii `"h<n>"`/`"v<n>"` dinainte de `"*"` pornesc din sursă. Pașii de după `"*"` se termină în destinație. Golul dintre ele se închide cu un segment orizontal, apoi unul vertical.
- Fundalul figurii e alb în ambele teme.
- Toate fișierele se citesc și se scriu în UTF-8 (diacritice).
- Schemele din pilot reproduc exact pinii din tabelul „Conectare” al paginii: LED pe **D10**, servo pe **D9**, DHT22 pe **GPIO 14**.

**Abateri de la spec, decise aici:**

- Șablonul de randare e `wiring_render.js` (o funcție trimisă la `page.evaluate`), nu `wiring_render.html`. Pagina se construiește cu `page.set_content` + `page.add_script_tag`.
- Figura folosește cale absolută (`/assets/images/wiring/<nume>.svg`) în loc de cale relativă. Motivul: plugin-ul i18n mută paginile EN sub `/en/`, iar raw HTML nu e rescris de MkDocs. Site-ul e servit din rădăcina domeniului, așa că calea absolută e corectă și pe RO, și pe EN.
- Fallback-ul raster WebP nu intră în plan. Se adaugă doar dacă pilotul arată o piesă stricată (vezi Task 5, Step 6).

## Review Focus

1. **Marker în bloc de cod** (de exemplu documentație care arată sintaxa): nu trebuie expandat. Testul e în Task 4.
2. **Nume de schemă greșit în marker**: build-ul pică cu un mesaj care numește pagina și schema, nu cu un 404 tăcut. Testul e în Task 4.
3. **Piesă rotită** (`"rotate": 90`): pinii și cutia de încadrare se rotesc odată cu piesa. Testele sunt în Task 1 și Task 2.
4. **Două piese de același tip** (două LED-uri): id-urile din SVG-urile interne nu se ciocnesc. Testul e în Task 2.
5. **Mediu fără Playwright** (CI) sau fără Chromium instalat: `uv run build` continuă cu un avertisment. Testele sunt în Task 3.

---

## File Structure

| Fișier | Rol |
|---|---|
| `src/ursoaia_edu_online/wiring.py` (nou) | Geometrie (pași, trasee, rotație, pini), compunere SVG, detectarea schemelor de regenerat, orchestrarea Playwright |
| `src/ursoaia_edu_online/wiring_render.js` (nou) | Funcție JS rulată în Chromium: piese → `{id, width, height, svg, css, pins}` |
| `src/ursoaia_edu_online/__init__.py` (modificat) | `build_diagrams()` + apel în `serve()`/`build()` |
| `hooks/wokwi.py` (nou) | Marker → `<figure class="wiring">` |
| `tests/test_wiring_geometry.py`, `tests/test_wiring_svg.py`, `tests/test_wiring_render.py`, `tests/test_wokwi_hook.py` (noi) | Teste |
| `pyproject.toml`, `uv.lock`, `.gitignore`, `mkdocs.yml`, `tailwind/input.css`, `custom_theme/assets/tailwind.css` (modificate) | Dependențe, script, hook, stil |
| `wiring/led-blinking/`, `wiring/servo/`, `wiring/esp32-dht22/` (noi) | Sursele pilotului |
| `docs/assets/images/wiring/*.svg` (noi, generate) | Ieșire |
| 4 pagini din pilot + `CLAUDE.md` (modificate) | Conținut și documentație |

---

### Task 1: Infrastructura de teste + geometria

**Files:**
- Modify: `pyproject.toml`
- Create: `src/ursoaia_edu_online/wiring.py`
- Create: `tests/test_wiring_geometry.py`

**Interfaces:**
- Produces (în `ursoaia_edu_online.wiring`):
  - `Point = tuple[float, float]`
  - `parse_step(step: str) -> Point`: ridică `ValueError` la pași invalizi
  - `route_points(start: Point, end: Point, steps: list[str]) -> list[Point]`
  - `rotate_point(p: Point, center: Point, degrees: float) -> Point`: sens orar în coordonate ecran (y în jos)
  - `pin_position(part: dict, size: Point, pin_xy: Point) -> Point`

- [ ] **Step 1: Adaugă pytest și grupul opțional pentru diagrame în `pyproject.toml`**

După blocul `dependencies = [...]`, adaugă:

```toml
[project.optional-dependencies]
diagrams = ["playwright>=1.47"]

[dependency-groups]
dev = ["pytest>=8.3"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

În `[project.scripts]`, adaugă:

```toml
build-diagrams = "ursoaia_edu_online:build_diagrams"
```

Rulează: `uv sync --extra diagrams`
Expected: instalează pytest și playwright, iar `uv.lock` se actualizează. Scriptul `build-diagrams` va eșua până la Task 3. Nu-l rula încă.

- [ ] **Step 2: Scrie testele (eșuează)**

`tests/test_wiring_geometry.py`:

```python
import pytest

from ursoaia_edu_online.wiring import parse_step, pin_position, rotate_point, route_points


def test_parse_step_horizontal_and_vertical():
    assert parse_step("h30") == (30.0, 0.0)
    assert parse_step("v-12.5") == (0.0, -12.5)


@pytest.mark.parametrize("bad", ["x10", "h", "v1e3", "*", ""])
def test_parse_step_rejects_garbage(bad):
    with pytest.raises(ValueError):
        parse_step(bad)


def test_route_without_steps_goes_horizontal_then_vertical():
    assert route_points((0, 0), (10, 20), []) == [(0, 0), (10, 0), (10, 20)]


def test_route_straight_line_has_no_extra_points():
    assert route_points((0, 5), (40, 5), []) == [(0, 5), (40, 5)]


def test_route_head_steps_from_source():
    assert route_points((0, 0), (50, -30), ["v-30"]) == [(0, 0), (0, -30), (50, -30)]


def test_route_tail_steps_end_in_target():
    # după "*": h50 trebuie să fie ultimul segment, care intră în pin
    pts = route_points((0, 0), (100, 60), ["v40", "*", "h50"])
    assert pts == [(0, 0), (0, 40), (50, 40), (50, 60), (100, 60)]


def test_rotate_point_clockwise_on_screen():
    assert rotate_point((10, 0), (0, 0), 90) == (0, 10)
    assert rotate_point((10, 0), (0, 0), 0) == (10, 0)


def test_pin_position_unrotated():
    part = {"top": 100, "left": 50}
    assert pin_position(part, (40, 60), (5, 7)) == (55, 107)


def test_pin_position_rotated_90_around_center():
    # piesă 40x20 la (0,0), centru (20,10); pinul (0,10) (stânga-mijloc) ajunge sus-mijloc
    part = {"top": 0, "left": 0, "rotate": 90}
    assert pin_position(part, (40, 20), (0, 10)) == (20, -10)
```

- [ ] **Step 3: Rulează testele ca să confirmi că eșuează**

Rulează: `uv run pytest tests/test_wiring_geometry.py -q`
Expected: FAIL cu `ModuleNotFoundError: No module named 'ursoaia_edu_online.wiring'`

- [ ] **Step 4: Implementează geometria**

`src/ursoaia_edu_online/wiring.py`:

```python
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
```

- [ ] **Step 5: Rulează testele**

Rulează: `uv run pytest tests/test_wiring_geometry.py -q`
Expected: PASS (toate)

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock src/ursoaia_edu_online/wiring.py tests/test_wiring_geometry.py
git commit -m "feat(wiring): wire routing and pin geometry for Wokwi diagrams"
```

---

### Task 2: Compunerea SVG-ului

**Files:**
- Modify: `src/ursoaia_edu_online/wiring.py`
- Create: `tests/test_wiring_svg.py`

**Interfaces:**
- Consumes: `route_points`, `rotate_point`, `pin_position`, `Point` (Task 1)
- Produces:
  - `prefix_ids(markup: str, prefix: str) -> str`
  - `scope_css(css: str, scope: str) -> str`
  - `place_svg(markup: str, x: float, y: float, w: float, h: float) -> str`
  - `compose_svg(diagram: dict, rendered: dict[str, dict]) -> str`. `rendered[id]` = `{"width": float, "height": float, "svg": str, "css": str, "pins": {nume: [x, y]}}`, adică exact ce întoarce `wiring_render.js` din Task 3. Ridică `ValueError` la piesă sau pin necunoscut ori la culoare invalidă.
  - `svg_size(svg_text: str) -> tuple[int, int]`: lățimea și înălțimea din `viewBox`

- [ ] **Step 1: Scrie testele (eșuează)**

`tests/test_wiring_svg.py`:

```python
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
```

- [ ] **Step 2: Rulează testele ca să confirmi că eșuează**

Rulează: `uv run pytest tests/test_wiring_svg.py -q`
Expected: FAIL cu `ImportError: cannot import name 'compose_svg'`

- [ ] **Step 3: Implementează compunerea**

Adaugă la `src/ursoaia_edu_online/wiring.py` (după `pin_position`):

```python
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
```

Verifică testul de rotație. LED-ul are 19×42 la (300,−100), deci centrul e (309.5,−79). Pinul A (12,42) e absolut (312,−58), cu offset (2.5, 21) față de centru. După rotația de 90°: (309.5−21, −79+2.5) = (288.5, −76.5).

- [ ] **Step 4: Rulează testele**

Rulează: `uv run pytest -q`
Expected: PASS (toate, inclusiv cele din Task 1)

- [ ] **Step 5: Commit**

```bash
git add src/ursoaia_edu_online/wiring.py tests/test_wiring_svg.py
git commit -m "feat(wiring): compose standalone SVG from rendered Wokwi parts"
```

---

### Task 3: Randarea în Chromium + `build_diagrams`

**Files:**
- Create: `src/ursoaia_edu_online/wiring_render.js`
- Modify: `src/ursoaia_edu_online/wiring.py`
- Modify: `src/ursoaia_edu_online/__init__.py`
- Modify: `.gitignore`
- Create: `tests/test_wiring_render.py`

**Interfaces:**
- Consumes: `compose_svg` (Task 2)
- Produces:
  - `stale_diagrams(wiring_dir: Path, out_dir: Path) -> list[tuple[str, Path, Path]]`: tupluri `(nume, diagram.json, <nume>.svg)`
  - `ensure_bundle(bundle: Path) -> Path`
  - `render_all(wiring_dir: Path, out_dir: Path, bundle: Path) -> int`: numărul de SVG-uri scrise. Întoarce 0 cu avertisment fără Playwright sau Chromium.
  - `ursoaia_edu_online.build_diagrams() -> None` (script `uv run build-diagrams`)
  - Constante în `__init__.py`: `WIRING_DIR = PROJECT_ROOT / "wiring"`, `WIRING_OUT = DOCS_DIR / "assets" / "images" / "wiring"`, `WOKWI_BUNDLE = PROJECT_ROOT / "tools" / "wokwi" / "wokwi-elements.bundle.js"`

- [ ] **Step 1: Scrie testele (eșuează)**

`tests/test_wiring_render.py`:

```python
import json
import os
import sys
import time

import pytest

from ursoaia_edu_online import wiring

LED_DIAGRAM = {
    "version": 1,
    "parts": [
        {"type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0, "attrs": {}},
        {"type": "wokwi-led", "id": "led1", "top": -100, "left": 300, "attrs": {"color": "red"}},
    ],
    "connections": [["uno:10", "led1:A", "green", ["v-50"]], ["led1:C", "uno:GND.2", "black", ["v300"]]],
}


def _write(tmp_path, name="led", diagram=LED_DIAGRAM):
    src = tmp_path / "wiring" / name
    src.mkdir(parents=True)
    (src / "diagram.json").write_text(json.dumps(diagram), "utf-8")
    return tmp_path / "wiring", tmp_path / "out"


def test_stale_diagrams_new_then_up_to_date(tmp_path):
    wiring_dir, out_dir = _write(tmp_path)
    todo = wiring.stale_diagrams(wiring_dir, out_dir)
    assert [t[0] for t in todo] == ["led"]
    out_dir.mkdir()
    svg = out_dir / "led.svg"
    svg.write_text("<svg/>", "utf-8")
    future = time.time() + 10
    os.utime(svg, (future, future))
    assert wiring.stale_diagrams(wiring_dir, out_dir) == []


def test_stale_diagrams_missing_dir_is_empty(tmp_path):
    assert wiring.stale_diagrams(tmp_path / "nope", tmp_path / "out") == []


def test_render_all_without_playwright_warns_and_skips(tmp_path, monkeypatch, capsys):
    wiring_dir, out_dir = _write(tmp_path)
    monkeypatch.setitem(sys.modules, "playwright", None)
    monkeypatch.setitem(sys.modules, "playwright.sync_api", None)
    assert wiring.render_all(wiring_dir, out_dir, tmp_path / "bundle.js") == 0
    assert "Playwright" in capsys.readouterr().err
    assert not out_dir.exists()


def test_render_all_without_chromium_warns_and_skips(tmp_path, monkeypatch, capsys):
    pytest.importorskip("playwright.sync_api")
    wiring_dir, out_dir = _write(tmp_path)

    def boom(_p):
        raise RuntimeError("Executable doesn't exist")

    monkeypatch.setattr(wiring, "_launch_browser", boom)
    monkeypatch.setattr(wiring, "ensure_bundle", lambda b: b)
    assert wiring.render_all(wiring_dir, out_dir, tmp_path / "bundle.js") == 0
    assert "playwright install chromium" in capsys.readouterr().err


def test_render_all_real_chromium(tmp_path):
    sync_api = pytest.importorskip("playwright.sync_api")
    try:
        with sync_api.sync_playwright() as p:
            p.chromium.launch().close()
    except Exception:
        pytest.skip("Chromium nu e instalat (uv run playwright install chromium)")
    wiring_dir, out_dir = _write(tmp_path)
    bundle = wiring.ensure_bundle(tmp_path / "bundle.js")
    assert wiring.render_all(wiring_dir, out_dir, bundle) == 1
    svg = (out_dir / "led.svg").read_text("utf-8")
    assert svg.startswith("<svg ") and 'stroke="green"' in svg and '<g id="p-uno"' in svg
    assert wiring.render_all(wiring_dir, out_dir, bundle) == 0  # la zi
```

- [ ] **Step 2: Rulează testele ca să confirmi că eșuează**

Rulează: `uv run pytest tests/test_wiring_render.py -q`
Expected: FAIL cu `AttributeError: module 'ursoaia_edu_online.wiring' has no attribute 'stale_diagrams'`

- [ ] **Step 3: Scrie funcția JS**

`src/ursoaia_edu_online/wiring_render.js`:

```js
// Rulat de Playwright cu page.evaluate(src, parts). Pagina are deja bundle-ul
// @wokwi/elements încărcat. Întoarce, pentru fiecare piesă, markup-ul SVG din
// shadow root, CSS-ul ei, dimensiunea randată și coordonatele pinilor.
async (parts) => {
  const out = [];
  for (const part of parts) {
    if (!customElements.get(part.type)) {
      throw new Error(`tip de piesă necunoscut: ${part.type} (${part.id})`);
    }
    const el = document.createElement(part.type);
    for (const [key, value] of Object.entries(part.attrs || {})) {
      el.setAttribute(key, String(value));
    }
    el.style.position = "absolute";
    document.body.appendChild(el);
    await el.updateComplete;
    const svg = el.shadowRoot && el.shadowRoot.querySelector("svg");
    if (!svg) throw new Error(`piesa ${part.id} nu are <svg>`);
    let css = "";
    for (const sheet of el.shadowRoot.adoptedStyleSheets || []) {
      for (const rule of sheet.cssRules) css += rule.cssText + "\n";
    }
    for (const style of el.shadowRoot.querySelectorAll("style")) css += style.textContent + "\n";
    const rect = svg.getBoundingClientRect();
    out.push({
      id: part.id,
      width: rect.width,
      height: rect.height,
      svg: svg.outerHTML,
      css,
      pins: Object.fromEntries((el.pinInfo || []).map((p) => [p.name, [p.x, p.y]])),
    });
    el.remove();
  }
  return out;
}
```

- [ ] **Step 4: Implementează orchestrarea în `wiring.py`**

Adaugă la începutul fișierului, lângă celelalte importuri:

```python
import json
import sys
import urllib.request
from pathlib import Path
```

și la final:

```python
WOKWI_ELEMENTS_VERSION = "1.9.1"
WOKWI_ELEMENTS_URL = (
    f"https://unpkg.com/@wokwi/elements@{WOKWI_ELEMENTS_VERSION}/dist/wokwi-elements.bundle.js"
)
_RENDER_JS = Path(__file__).with_name("wiring_render.js")


def _warn(msg: str) -> None:
    print(f"Wiring: {msg}", file=sys.stderr)


def stale_diagrams(wiring_dir: Path, out_dir: Path) -> list[tuple[str, Path, Path]]:
    if not wiring_dir.is_dir():
        return []
    todo = []
    for src in sorted(wiring_dir.glob("*/diagram.json")):
        name = src.parent.name
        dst = out_dir / f"{name}.svg"
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            todo.append((name, src, dst))
    return todo


def ensure_bundle(bundle: Path) -> Path:
    if bundle.exists():
        return bundle
    bundle.parent.mkdir(parents=True, exist_ok=True)
    _warn(f"descarc @wokwi/elements {WOKWI_ELEMENTS_VERSION}…")
    urllib.request.urlretrieve(WOKWI_ELEMENTS_URL, bundle)  # noqa: S310 — URL fixat
    return bundle


def _launch_browser(playwright):
    return playwright.chromium.launch()


def render_all(wiring_dir: Path, out_dir: Path, bundle: Path) -> int:
    todo = stale_diagrams(wiring_dir, out_dir)
    if not todo:
        _warn("0 scheme de regenerat (la zi)")
        return 0
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        _warn(
            f"{len(todo)} scheme neactualizate: lipsește Playwright "
            "(uv sync --extra diagrams && uv run playwright install chromium). Folosesc SVG-urile existente."
        )
        return 0

    bundle = ensure_bundle(bundle)
    render_js = _RENDER_JS.read_text("utf-8")
    written = 0
    with sync_playwright() as p:
        try:
            browser = _launch_browser(p)
        except Exception as exc:  # browser lipsă / sandbox
            _warn(
                f"{len(todo)} scheme neactualizate: Chromium nu pornește ({exc.__class__.__name__}). "
                "Rulează `uv run playwright install chromium`."
            )
            return 0
        try:
            page = browser.new_page()
            page.set_content('<!doctype html><meta charset="utf-8"><body></body>')
            page.add_script_tag(path=str(bundle))
            for name, src, dst in todo:
                try:
                    diagram = json.loads(src.read_text("utf-8"))
                    items = page.evaluate(render_js, diagram["parts"])
                    svg = compose_svg(diagram, {item["id"]: item for item in items})
                except Exception as exc:
                    raise RuntimeError(f"wiring/{name}/diagram.json: {exc}") from exc
                dst.parent.mkdir(parents=True, exist_ok=True)
                dst.write_text(svg, "utf-8")
                written += 1
        finally:
            browser.close()
    _warn(f"{written} scheme regenerate")
    return written
```

- [ ] **Step 5: Conectează pasul în `src/ursoaia_edu_online/__init__.py`**

Sub `RASTER_EXTS = {...}`, adaugă:

```python
WIRING_DIR = PROJECT_ROOT / "wiring"
WIRING_OUT = DOCS_DIR / "assets" / "images" / "wiring"
WOKWI_BUNDLE = PROJECT_ROOT / "tools" / "wokwi" / "wokwi-elements.bundle.js"
```

Înainte de `def serve()`, adaugă:

```python
def build_diagrams() -> None:
    """Regenerează SVG-urile Wokwi din wiring/*/diagram.json (vezi wiring.py)."""
    from ursoaia_edu_online.wiring import render_all

    render_all(WIRING_DIR, WIRING_OUT, WOKWI_BUNDLE)
```

În `serve()` și în `build()`, după blocul `build_images()`, adaugă:

```python
    if os.environ.get("URSOAIA_SKIP_DIAGRAMS") != "1":
        build_diagrams()
```

Actualizează docstring-ul modulului: „`build_diagrams` renders Wokwi wiring diagrams from `wiring/*/diagram.json` into `docs/assets/images/wiring/*.svg`”.

În `.gitignore`, sub `tailwind/bin/`, adaugă:

```
tools/wokwi/
```

- [ ] **Step 6: Instalează Chromium și rulează testele**

Rulează: `uv run playwright install chromium && uv run pytest -q`
Expected: PASS (toate). `test_render_all_real_chromium` rulează, nu e skip.

- [ ] **Step 7: Verifică CLI-ul fără scheme**

Rulează: `uv run build-diagrams`
Expected: stderr `Wiring: 0 scheme de regenerat (la zi)` (folderul `wiring/` nu există încă), exit 0.

- [ ] **Step 8: Commit**

```bash
git add src/ursoaia_edu_online/wiring_render.js src/ursoaia_edu_online/wiring.py src/ursoaia_edu_online/__init__.py .gitignore tests/test_wiring_render.py
git commit -m "feat(wiring): render Wokwi diagrams to SVG with headless Chromium"
```

---

### Task 4: Hook-ul MkDocs și stilul figurii

**Files:**
- Create: `hooks/wokwi.py`
- Modify: `mkdocs.yml` (secțiunea `hooks:`)
- Modify: `tailwind/input.css` (după regula `.prose img`, ~linia 232)
- Modify: `custom_theme/assets/tailwind.css` (regenerat)
- Create: `tests/test_wokwi_hook.py`

**Interfaces:**
- Consumes: `svg_size(svg_text) -> (int, int)` (Task 2)
- Produces: `expand_markers(markdown: str, *, src_uri: str, locale: str, title: str | None, docs_dir: str | Path) -> str` și `on_page_markdown(markdown, page, config, files)`

- [ ] **Step 1: Scrie testele (eșuează)**

`tests/test_wokwi_hook.py`:

```python
import importlib.util
from pathlib import Path

import pytest
from mkdocs.exceptions import PluginError

_spec = importlib.util.spec_from_file_location(
    "wokwi_hook", Path(__file__).resolve().parents[1] / "hooks" / "wokwi.py"
)
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)

SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-16 -116 351.2 334.4"></svg>'


@pytest.fixture
def docs(tmp_path):
    out = tmp_path / "assets" / "images" / "wiring"
    out.mkdir(parents=True)
    (out / "led-blinking.svg").write_text(SVG, "utf-8")
    return tmp_path


def expand(md, docs, locale="ro", title="LED intermitent"):
    return hook.expand_markers(
        md, src_uri="projects/arduino/starter_kit/02-led-blinking.md",
        locale=locale, title=title, docs_dir=docs,
    )


def test_marker_becomes_figure_ro(docs):
    out = expand("## Conectare\n\n[[wokwi:led-blinking]]\n\nText", docs)
    assert '<figure class="wiring">' in out
    assert 'src="/assets/images/wiring/led-blinking.svg"' in out
    assert 'width="351" height="334"' in out
    assert 'alt="Schema de conectare: LED intermitent"' in out
    assert "<figcaption>Schema de conectare</figcaption>" in out
    assert "wokwi.com" not in out
    assert out.startswith("## Conectare\n") and out.endswith("\nText")


def test_marker_with_project_id_adds_simulate_link_en(docs):
    out = expand("[[wokwi:led-blinking|412345678901234567]]", docs, locale="en", title="LED Blink")
    assert 'href="https://wokwi.com/projects/412345678901234567"' in out
    assert "Simulate in Wokwi" in out and "Wiring diagram" in out


def test_marker_inside_code_fence_is_left_alone(docs):
    md = "```text\n[[wokwi:led-blinking]]\n```\n"
    assert expand(md, docs) == md


def test_unknown_diagram_fails_with_page_and_name(docs):
    with pytest.raises(PluginError, match=r"02-led-blinking\.md.*nu-exista"):
        expand("[[wokwi:nu-exista]]", docs)


def test_title_is_html_escaped(docs):
    out = expand("[[wokwi:led-blinking]]", docs, title='Senzor "DHT22" <ESP32>')
    assert "&quot;DHT22&quot; &lt;ESP32&gt;" in out


def test_marker_must_be_alone_on_line(docs):
    md = "vezi [[wokwi:led-blinking]] aici"
    assert expand(md, docs) == md
```

- [ ] **Step 2: Rulează testele ca să confirmi că eșuează**

Rulează: `uv run pytest tests/test_wokwi_hook.py -q`
Expected: FAIL cu `FileNotFoundError` (lipsește `hooks/wokwi.py`)

- [ ] **Step 3: Implementează hook-ul**

`hooks/wokwi.py`:

```python
"""MkDocs hook: expand Wokwi wiring markers into a figure.

A line containing only ``[[wokwi:<name>]]`` or ``[[wokwi:<name>|<project-id>]]``
becomes a ``<figure class="wiring">`` with the SVG generated by
``uv run build-diagrams`` (``docs/assets/images/wiring/<name>.svg``) and, when a
project id is given, a "Simulate in Wokwi" link. Markers inside fenced code
blocks are left untouched. A marker whose SVG is missing fails the build.

The image path is absolute (``/assets/...``): the i18n plugin serves English
pages under ``/en/`` and raw HTML is not rewritten by MkDocs, while the site is
always served from the domain root.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from mkdocs.exceptions import PluginError

_MARKER_RE = re.compile(r"^\[\[wokwi:([a-z0-9-]+)(?:\|(\d+))?\]\]\s*$")
_FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
_VIEWBOX_RE = re.compile(r'viewBox="\s*-?[\d.]+[\s,]+-?[\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)\s*"')
_SVG_DIR = "assets/images/wiring"
_TEXTS = {
    "ro": ("Schema de conectare", "Simulează în Wokwi"),
    "en": ("Wiring diagram", "Simulate in Wokwi"),
}


def _figure(name: str, project_id: str | None, *, svg_path: Path, label: str, sim: str, title: str | None) -> str:
    m = _VIEWBOX_RE.search(svg_path.read_text("utf-8")[:4000])
    size = f' width="{round(float(m.group(1)))}" height="{round(float(m.group(2)))}"' if m else ""
    alt = html.escape(f"{label}: {title}" if title else label)
    caption = label
    if project_id:
        caption += (
            f' · <a href="https://wokwi.com/projects/{project_id}" target="_blank" rel="noopener">{sim}</a>'
        )
    return (
        '<figure class="wiring">'
        f'<img src="/{_SVG_DIR}/{name}.svg" alt="{alt}"{size}>'
        f"<figcaption>{caption}</figcaption>"
        "</figure>"
    )


def expand_markers(markdown: str, *, src_uri: str, locale: str, title: str | None, docs_dir) -> str:
    label, sim = _TEXTS.get(locale, _TEXTS["ro"])
    fence: str | None = None
    out: list[str] = []
    for line in markdown.split("\n"):
        f = _FENCE_RE.match(line)
        if f:
            token = f.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            out.append(line)
            continue
        m = None if fence else _MARKER_RE.match(line)
        if not m:
            out.append(line)
            continue
        name, project_id = m.groups()
        svg_path = Path(docs_dir) / _SVG_DIR / f"{name}.svg"
        if not svg_path.is_file():
            raise PluginError(
                f"{src_uri}: schema Wokwi „{name}” lipsește ({svg_path}). "
                f"Creează wiring/{name}/diagram.json și rulează `uv run build-diagrams`."
            )
        out.append(_figure(name, project_id, svg_path=svg_path, label=label, sim=sim, title=title))
    return "\n".join(out)


def on_page_markdown(markdown: str, page, config, files) -> str:
    src_uri = page.file.src_uri
    locale = getattr(page.file, "locale", None) or ("en" if src_uri.endswith(".en.md") else "ro")
    return expand_markers(
        markdown, src_uri=src_uri, locale=locale, title=page.title, docs_dir=config["docs_dir"]
    )
```

Hook-ul nu importă din `ursoaia_edu_online`, ca să meargă și cu `mkdocs build` simplu. Parsarea `viewBox` e duplicată intenționat, pe 3 rânduri.

- [ ] **Step 4: Rulează testele**

Rulează: `uv run pytest -q`
Expected: PASS (toate)

- [ ] **Step 5: Înregistrează hook-ul în `mkdocs.yml`**

```yaml
hooks:
  - hooks/copy_well_known.py
  - hooks/lazy_images.py
  - hooks/wokwi.py
```

- [ ] **Step 6: Adaugă stilul figurii în `tailwind/input.css`**

Imediat după regula `.prose img { … }`:

```css
/* Scheme de conectare Wokwi (hooks/wokwi.py): fundal alb și în dark mode, piesele Wokwi sunt desenate pentru fundal deschis. */
.prose figure.wiring {
  margin: 2rem 0;
  padding: 1rem;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  overflow-x: auto;
  text-align: center;
}
.dark .prose figure.wiring { border-color: rgba(255,255,255,0.08); }
.prose figure.wiring img {
  display: inline-block;
  max-width: 100%;
  height: auto;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
}
.prose figure.wiring figcaption {
  margin-top: 0.75rem;
  font-size: 0.8125rem;
  color: #6b7280;
}
.prose figure.wiring figcaption a { font-weight: 500; }
```

Rulează: `uv run build-css`
Expected: `custom_theme/assets/tailwind.css` regenerat. Verifică cu `grep -c "figure.wiring" custom_theme/assets/tailwind.css` (≥ 1).

- [ ] **Step 7: Build strict fără markere**

Rulează: `URSOAIA_SKIP_DIAGRAMS=1 uv run build --strict`
Expected: build reușit. Nicio pagină nu are încă markere.

- [ ] **Step 8: Commit**

```bash
git add hooks/wokwi.py mkdocs.yml tailwind/input.css custom_theme/assets/tailwind.css tests/test_wokwi_hook.py
git commit -m "feat(wiring): MkDocs hook for [[wokwi:…]] figures"
```

---

### Task 5: Pilotul — 3 scheme pe 4 pagini

**Files:**
- Create: `wiring/led-blinking/diagram.json`, `wiring/led-blinking/sketch.ino`
- Create: `wiring/servo/diagram.json`, `wiring/servo/sketch.ino`
- Create: `wiring/esp32-dht22/diagram.json`, `wiring/esp32-dht22/main.py`
- Create (generate): `docs/assets/images/wiring/{led-blinking,servo,esp32-dht22}.svg`
- Modify: `docs/projects/arduino/starter_kit/02-led-blinking.md`, `docs/projects/arduino/starter_kit/08-servo.md`, `docs/projects/esp32/temperature.md`, `docs/projects/esp32/temperature.en.md`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: `uv run build-diagrams` (Task 3), markerul `[[wokwi:<nume>]]` (Task 4)

- [ ] **Step 1: `wiring/led-blinking/diagram.json`** (LED pe **D10**, ca în tabelul paginii)

```json
{
  "version": 1,
  "author": "ursoaia-edu.online",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0, "attrs": {} },
    { "type": "wokwi-resistor", "id": "r1", "top": -70, "left": 190, "attrs": { "value": "220" } },
    { "type": "wokwi-led", "id": "led1", "top": -130, "left": 310, "attrs": { "color": "red" } }
  ],
  "connections": [
    ["uno:10", "r1:1", "green", ["v-73.35"]],
    ["r1:2", "led1:A", "green", []],
    ["led1:C", "uno:GND.2", "black", ["v300"]]
  ],
  "dependencies": {}
}
```

`wiring/led-blinking/sketch.ino`: copiază neschimbat blocul de cod Arduino din secțiunea `## Cod` a paginii `docs/projects/arduino/starter_kit/02-led-blinking.md`.

- [ ] **Step 2: `wiring/servo/diagram.json`** (semnal pe **D9**)

```json
{
  "version": 1,
  "author": "ursoaia-edu.online",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0, "attrs": {} },
    { "type": "wokwi-servo", "id": "sv", "top": 10, "left": 380, "attrs": {} }
  ],
  "connections": [
    ["uno:GND.2", "sv:GND", "black", ["v40", "*", "h50"]],
    ["uno:5V", "sv:V+", "red", ["v55", "*", "h40"]],
    ["uno:9", "sv:PWM", "orange", ["v-20", "h-180", "v290", "*", "h30"]]
  ],
  "dependencies": {}
}
```

`wiring/servo/sketch.ino`: blocul de cod din `## Cod` al paginii `08-servo.md`.

- [ ] **Step 3: `wiring/esp32-dht22/diagram.json`** (DATA pe **GPIO 14** = pinul `D14`, pull-up 10 kΩ)

```json
{
  "version": 1,
  "author": "ursoaia-edu.online",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-esp32-devkit-v1", "id": "esp", "top": 0, "left": 0, "attrs": {} },
    { "type": "wokwi-dht22", "id": "dht", "top": -40, "left": -170, "attrs": {} },
    { "type": "wokwi-resistor", "id": "r1", "top": 150, "left": -260, "attrs": { "value": "10000" } }
  ],
  "connections": [
    ["esp:D14", "dht:SDA", "blue", ["h-30"]],
    ["esp:GND.2", "dht:GND", "black", ["h-15"]],
    ["esp:3V3", "dht:VCC", "red", ["h15", "v50"]],
    ["r1:2", "dht:VCC", "red", ["h20"]],
    ["r1:1", "dht:SDA", "blue", ["v-50"]]
  ],
  "dependencies": {}
}
```

`wiring/esp32-dht22/main.py`: blocul MicroPython principal din `docs/projects/esp32/temperature.md`. Dacă pagina folosește alt pin decât 14 în cod, oprește-te și raportează diferența.

- [ ] **Step 4: Generează și inspectează SVG-urile**

Rulează: `uv run build-diagrams`
Expected: `Wiring: 3 scheme regenerate`

Deschide fiecare SVG (de exemplu `qlmanage -t -s 900 -o /tmp docs/assets/images/wiring/*.svg`, apoi citește PNG-urile). Verifică, pentru fiecare:
- toate piesele sunt vizibile și complete (plăcile cu headere, LED-ul roșu, servo-ul cu brațul, DHT22);
- fiecare fir pornește și se termină exact pe pinul corect (comparat cu tabelul „Conectare”);
- firele nu trec peste corpul pieselor. O încrucișare între fire de culori diferite e acceptabilă.

Coordonatele de mai sus sunt un punct de pornire. Ajustează `top`/`left` și pașii de traseu până arată curat. Reia `uv run build-diagrams` după fiecare modificare (JSON-ul mai nou declanșează regenerarea).

- [ ] **Step 5: Verificarea cu wokwi.com**

Deschide `https://wokwi.com/projects/new/arduino-uno` (respectiv `/esp32`), lipește `diagram.json` în tab-ul diagram.json și compară vizual cu SVG-ul. Pe wokwi.com distanța rămasă între capete s-ar putea închide altfel decât „orizontal, apoi vertical”. În cazul ăsta, notează diferența în spec (secțiunea „Traseele firelor”) și adaugă pași expliciți în JSON, ca ambele să arate la fel. Nu schimba regula din `route_points` fără un test nou.

- [ ] **Step 6: Decizia pentru fallback raster**

Dacă o piesă arată stricat în SVG, dar corect în Chromium (stiluri sau filtre pierdute), oprește-te și raportează piesa și simptomul. Fallback-ul WebP din spec se planifică separat. Dacă totul arată corect, nu faci nimic.

- [ ] **Step 7: Pune markerele în pagini**

`02-led-blinking.md` și `08-servo.md`: în `## Conectare`, imediat după tabel, pe un rând separat, cu rânduri goale înainte și după:

```
[[wokwi:led-blinking]]
```

(respectiv `[[wokwi:servo]]`). Blocul ASCII ```` ```board ```` rămâne.

`esp32/temperature.md`: înlocuiește subsecțiunea `### Scheme de conectare` (cele două imagini preluate) cu:

```
### Schema de conectare

[[wokwi:esp32-dht22]]
```

`esp32/temperature.en.md`: aceeași înlocuire, cu heading-ul `### Wiring diagram`. Fișierele imagine vechi (`ESP32-interfacing-with-dht11.webp`, `esp32-micropython-dht22-temperature-humidity-sensor-wiring-diagram.jpg` + `.webp`) **nu se șterg**. Le listezi utilizatorului pentru aprobare. Verifică cu `grep -rn "ESP32-interfacing-with-dht11\|dht22-temperature-humidity-sensor-wiring" docs/` dacă le mai folosește altă pagină.

- [ ] **Step 8: Build strict complet**

Rulează: `uv run build --strict`
Expected: build reușit, `Wiring: 0 scheme de regenerat (la zi)`.

Rulează: `URSOAIA_SKIP_DIAGRAMS=1 uv run build --strict`
Expected: build reușit (scenariul CI).

Verifică HTML-ul: `grep -o '<figure class="wiring">[^§]*</figure>' site/projects/arduino/starter_kit/02-led-blinking/index.html | head -c 400`
Expected: `<img loading="lazy" decoding="async" src="/assets/images/wiring/led-blinking.svg" alt="Schema de conectare: …" width=… height=…>`.

Verifică și pagina EN: `grep -c 'Wiring diagram' site/en/projects/esp32/temperature/index.html` (≥ 1) și `ls site/assets/images/wiring/` (3 SVG-uri).

- [ ] **Step 9: Verificare vizuală în browser**

Rulează `uv run serve` și deschide cele 3 pagini RO + pagina EN de temperatură, la desktop și la 375 px lățime, în light și dark. Expected: figura are fundal alb și în dark mode, nu produce scroll orizontal al paginii, iar legenda se citește.

- [ ] **Step 10: Actualizează `CLAUDE.md`**

Adaugă după secțiunea „Tailwind bundle (`tailwind/`)”:

````markdown
### Scheme de conectare Wokwi (`wiring/`)

Fiecare schemă de montaj e un folder `wiring/<nume>/` cu `diagram.json` (format Wokwi original, se poate lipi direct pe wokwi.com) și codul proiectului (`sketch.ino` / `main.py`). `uv run build` (sau `uv run build-diagrams`) randează piesele `@wokwi/elements@1.9.1` în Chromium headless și scrie `docs/assets/images/wiring/<nume>.svg`. SVG-urile sunt **commit-uite**: CI-ul nu are Chromium și sare pasul cu un avertisment.

```bash
uv sync --extra diagrams && uv run playwright install chromium   # o singură dată
uv run build-diagrams      # regenerează doar schemele cu diagram.json mai nou
uv run pytest              # teste pentru geometrie, SVG, hook
```

În pagină, pe un rând separat în secțiunea „Conectare”: `[[wokwi:<nume>]]` sau `[[wokwi:<nume>|<id-proiect-wokwi>]]` (adaugă butonul „Simulează în Wokwi”). `hooks/wokwi.py` îl transformă în figură; un nume inexistent pică build-ul. Pinii din `diagram.json` trebuie să coincidă cu tabelul „Conectare” al paginii. Schemdraw (scheme electrice) doar cu aprobare explicită.
````

În paragraful despre `serve`/`build`, adaugă `build_diagrams` la lista pașilor rulați înainte de MkDocs și `URSOAIA_SKIP_DIAGRAMS=1` la variabilele de skip.

- [ ] **Step 11: Commit**

```bash
git add wiring docs/assets/images/wiring docs/projects/arduino/starter_kit/02-led-blinking.md docs/projects/arduino/starter_kit/08-servo.md docs/projects/esp32/temperature.md docs/projects/esp32/temperature.en.md CLAUDE.md
git commit -m "content(wiring): Wokwi diagrams for LED blink, servo and ESP32 DHT22 pilot"
```

---

## După pilot (plan separat)

Restul paginilor intră în loturi, după aprobarea pilotului: starter kit 01–25 fără 02 și 08, ESP32 restul, `led_cube`, `lopy/lorawan_node`. Fiecare lot are același model ca Task 5, Steps 1–8, plus un commit. ID-urile de simulare se adaugă în markere pe măsură ce utilizatorul salvează proiectele pe wokwi.com.
