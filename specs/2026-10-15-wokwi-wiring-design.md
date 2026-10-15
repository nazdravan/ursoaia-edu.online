# Scheme de conectare Wokwi pe paginile de proiecte — design

Data: 2026-10-15 · Branch: `wokwi-wiring`

## Scop

Paginile de proiecte (Arduino starter kit, ESP32, LED cube, LoPy) au doar tabele „Conectare”, fără schemă desenată. Câteva pagini ESP32 folosesc imagini preluate de pe alte site-uri. Vrem pentru fiecare proiect o schemă de montaj proprie, în stil Wokwi: plăcile și piesele reale, cu fire colorate. Opțional, pagina are și un link către simularea proiectului pe wokwi.com.

Criterii de succes:

- Fiecare pagină de proiect are o schemă de montaj generată din `diagram.json`, servită ca SVG static, fără JS pe site.
- `uv run build --strict` trece. CI-ul (`.github/workflows/deploy.yml`) nu are nevoie de Chromium.
- Același `diagram.json` se lipește pe wokwi.com și dă același circuit.

În afara scopului: scheme electrice cu Schemdraw. Le folosim doar în cazuri extreme și doar după aprobare explicită.

## Decizii luate

| Întrebare | Decizie |
|---|---|
| Unealtă | Wokwi (`diagram.json` + piesele din `@wokwi/elements`) |
| Randare | SVG static generat la build cu Chromium headless (Playwright); SVG-urile se commit-uiesc |
| Simulare | Buton opțional „Simulează în Wokwi”, afișat doar când pagina dă un ID de proiect |
| Ordine | Pilot pe 3 pagini (`starter_kit/02-led-blinking`, `starter_kit/08-servo`, `esp32/temperature`), apoi restul în loturi |

## Structura fișierelor

```
wiring/                                  # sursa schemelor (în afara docs/, nu se publică)
  led-blinking/
    diagram.json                         # format Wokwi original
    sketch.ino                           # sau main.py pentru MicroPython (pentru proiectul de simulare)
  servo/ …
  esp32-dht22/ …
tools/wokwi/                             # gitignored
  wokwi-elements.bundle.js               # descărcat la prima rulare, versiune fixată
src/ursoaia_edu_online/
  __init__.py                            # + build_diagrams(), apelat din serve/build
  wiring_render.html                     # pagina-șablon pe care o încarcă Chromium
hooks/
  wokwi.py                               # transformă markerul [[wokwi:…]] în figură
docs/assets/images/wiring/
  led-blinking.svg                       # generat, commit-uit
```

Numele schemei este numele folderului din `wiring/`, în kebab-case. O schemă poate fi folosită de mai multe pagini, de exemplu varianta RO și EN.

## `diagram.json`

Formatul este cel al Wokwi, fără câmpuri proprii:

```json
{
  "version": 1,
  "author": "ursoaia-edu.online",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0, "attrs": {} },
    { "type": "wokwi-resistor", "id": "r1", "top": -60, "left": 170, "attrs": { "value": "220" } },
    { "type": "wokwi-led", "id": "led1", "top": -110, "left": 300, "attrs": { "color": "red" } }
  ],
  "connections": [
    ["uno:13", "r1:1", "green", ["v-90"]],
    ["r1:2", "led1:A", "green", []],
    ["led1:C", "uno:GND.2", "black", ["v230", "*", "v20"]]
  ],
  "dependencies": {}
}
```

Câmpuri folosite de renderer: `parts[].type/id/top/left/rotate/attrs` și `connections[]` = `[from, to, culoare, traseu]`.

## Randarea (`build_diagrams`)

Pasul rulează în `serve` și `build`, după `build_css` și `build_images`, și există și ca script separat, `uv run build-diagrams`.

1. Pentru fiecare `wiring/<nume>/diagram.json`, compară timpul de modificare cu `docs/assets/images/wiring/<nume>.svg`. Sare peste schemele la zi.
2. Dacă nu există nimic de regenerat, se oprește fără să pornească Chromium.
3. Dacă Playwright lipsește, afișează un avertisment și sare pasul. La fel dacă e setat `URSOAIA_SKIP_DIAGRAMS=1`. Build-ul continuă cu SVG-urile commit-uite, deci CI-ul rămâne neschimbat.
4. Altfel pornește Chromium headless o singură dată pentru toate schemele. Încarcă `wiring_render.html`, care include `tools/wokwi/wokwi-elements.bundle.js` printr-un `<script>` local. Pentru fiecare schemă:
   - creează elementele `wokwi-*` cu `top/left/rotate/attrs` și așteaptă `updateComplete`;
   - calculează coordonatele pinilor din `el.pinInfo`, ținând cont de `rotate`;
   - desenează firele după traseu (vezi mai jos);
   - serializează rezultatul într-un singur SVG. Pentru fiecare piesă, `<svg>`-ul din shadow root devine un `<svg x y width height>` imbricat, iar stilurile din shadow root sunt copiate într-un `<style>` cu prefix unic per piesă. Firele sunt `<path>` deasupra pieselor. `viewBox` = cutia tuturor pieselor și firelor, cu 16 px margine. Fundalul e alb.
5. Scrie `docs/assets/images/wiring/<nume>.svg`.

Dependențe noi: grupul opțional `diagrams = ["playwright>=1.47"]` în `pyproject.toml`. Instalare locală: `uv sync --extra diagrams && uv run playwright install chromium`. Bundle-ul `@wokwi/elements@1.9.1` se descarcă de pe unpkg la prima rulare, după modelul binarului Tailwind.

### Traseele firelor

Folosim sintaxa Wokwi: o listă de pași `"v<n>"` / `"h<n>"`, deplasări relative în px. Semantica de mai jos a fost verificată pe wokwi.com pe 2026-10-15, prin citirea traseelor desenate de editor. Cazurile sunt fixate în `tests/test_wiring_geometry.py::test_route_matches_wokwi`.

- Pașii dinainte de `"*"` pornesc de la pinul sursă și se aplică în ordine.
- Pașii de după `"*"` pornesc din pinul destinație. Coada începe în destinație + suma pașilor și îi parcurge în ordine, cu semn invers, până în pin. De exemplu, `["*", "h-30"]` intră în pin din stânga, pe ultimii 30 px.
- Golul dintre cap și coadă se închide cu un L. Dacă există coadă, ultimul segment al L-ului e perpendicular pe primul pas al cozii. Fără coadă, L-ul continuă orientarea ultimului pas din cap. Fără niciun pas, primul segment e orizontal.

### Fallback raster

Dacă o piesă nu se serializează corect ca SVG (stiluri sau filtre pierdute), schema respectivă se poate marca în `wiring/<nume>/render.json` cu `{ "format": "webp" }`. Atunci se face screenshot la 2x și se scrie `<nume>.webp`. Hook-ul alege fișierul existent. Fallback-ul se implementează doar dacă pilotul îl cere.

## În pagini: markerul și hook-ul

În Markdown, în secțiunea „Conectare”, pe un rând separat:

```
[[wokwi:led-blinking]]
[[wokwi:led-blinking|412345678901234567]]
```

`hooks/wokwi.py` (`on_page_markdown`) înlocuiește markerul cu:

```html
<figure class="wiring">
  <img src="…/assets/images/wiring/led-blinking.svg" alt="Schema de conectare: LED intermitent" width="…" height="…">
  <figcaption>Schema de conectare · <a href="https://wokwi.com/projects/412345678901234567" target="_blank" rel="noopener">Simulează în Wokwi</a></figcaption>
</figure>
```

- Calea relativă se calculează din `page.file.src_uri`.
- Textele depind de limba paginii: `.en.md` → „Wiring diagram” / „Simulate in Wokwi”, altfel română.
- `alt` folosește titlul paginii.
- `width`/`height` vin din `viewBox`-ul SVG-ului, ca să nu existe layout shift.
- Dacă SVG-ul lipsește, hook-ul aruncă o eroare care pică build-ul cu numele schemei. Așa `--strict` prinde markerele greșite.
- `hooks/lazy_images.py` adaugă `loading="lazy"` automat. Nu e nevoie de `<picture>`, pentru că sursa e SVG.

Stil (în `tailwind/input.css`): `.wiring` are fundal alb în ambele teme, colțuri rotunjite, padding, `max-width: 100%` și overflow-x auto pe ecrane mici. Legenda e mică, în culoarea „muted”.

Linkul de simulare: proiectul îl salvează utilizatorul pe wokwi.com (cont gratuit), lipind `diagram.json` și `sketch.ino`/`main.py` din `wiring/<nume>/`. Eu adaug apoi ID-ul în marker.

## Pilot

| Pagină | Schemă |
|---|---|
| `docs/projects/arduino/starter_kit/02-led-blinking.md` | `led-blinking` |
| `docs/projects/arduino/starter_kit/08-servo.md` | `servo` |
| `docs/projects/esp32/temperature.md` + `.en.md` | `esp32-dht22` |

La `esp32/temperature`, schema nouă înlocuiește cele două imagini preluate (`ESP32-interfacing-with-dht11.webp` și `esp32-micropython-dht22-…-wiring-diagram.jpg`). Fișierele vechi se șterg doar după aprobare.

## Testare

- `uv run build-diagrams` generează cele 3 SVG-uri. O a doua rulare nu regenerează nimic.
- `URSOAIA_SKIP_DIAGRAMS=1 uv run build --strict` trece, adică exact scenariul din CI.
- `uv run build --strict` trece. Un marker cu nume inexistent pică build-ul cu un mesaj clar.
- Verificare vizuală în `uv run serve`: cele 3 pagini, light și dark, desktop și 375 px lățime.
- Comparare manuală cu wokwi.com: `diagram.json` lipit în editor arată aceleași fire.

## După pilot

Restul paginilor se fac în loturi: starter kit 01–25 minus pilotul, ESP32 restul, `led_cube`, `lopy/lorawan_node`. Fiecare lot are commit-ul lui. Paginile fără montaj fizic nu primesc schemă (`windows_setup`, `17-serial-monitor` dacă are doar USB, indexurile). `CLAUDE.md` din repo se actualizează cu secțiunea „Scheme Wokwi”: comenzi, structură, marker.
