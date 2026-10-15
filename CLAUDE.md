# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A MkDocs site (<https://ursoaia-edu.online>) documenting hands-on electronics / IoT education projects (Arduino, ESP32, LoPy, Raspberry Pi). The Python project is managed with `uv` and targets Python 3.12.

## Commands

Dependencies and environment are managed by `uv` (see `pyproject.toml`, `uv.lock`, `.venv/`).

```bash
# Install / sync dependencies into .venv (also installs the local package
# defined by pyproject.toml so the `serve` / `build` console scripts register).
uv sync

# Serve the site locally with live reload (http://127.0.0.1:8000)
uv run serve            # equivalent: uv run mkdocs serve

# Produce the static site in ./site
uv run build            # equivalent: uv run mkdocs build

# Strict build (fail on warnings, e.g. broken links / missing nav files)
uv run build --strict   # equivalent: uv run mkdocs build --strict

# Rebuild only the Tailwind bundle (auto-runs as part of serve/build)
uv run build-css

# Regenerate .webp siblings for raster images (auto-runs as part of serve/build)
uv run build-images
```

The `serve` and `build` shortcuts come from `[project.scripts]` in `pyproject.toml`, wired to `src/ursoaia_edu_online/__init__.py`. They run `build_css` (Tailwind standalone CLI → `custom_theme/assets/tailwind.css`) `build_images` (Pillow → `.webp` siblings of every `*.jpg/*.png` under `docs/`) and `build_diagrams` (Wokwi wiring diagrams → SVG, see below) first, then forward argv to `mkdocs.__main__.cli`. Set `URSOAIA_SKIP_CSS=1`, `URSOAIA_SKIP_IMAGES=1` or `URSOAIA_SKIP_DIAGRAMS=1` to skip steps individually.

The `hooks/lazy_images.py` MkDocs hook then wraps each `<img>` whose src ends in jpg/jpeg/png in a `<picture>` element so browsers prefer the .webp variant. Combined effect: ~80% smaller image payload (15.4 MB → 3.2 MB on the current asset set).

### Tailwind bundle (`tailwind/`)

The site's CSS is compiled by the Tailwind v3 standalone CLI (single binary, no Node toolchain). On first run, `build_css` downloads the binary from GitHub releases into `tailwind/bin/` (gitignored).

- `tailwind/tailwind.config.js` — content paths cover `custom_theme/**/*.html` and `docs/**/*.{md,html}`; the `@tailwindcss/typography` plugin is bundled into the standalone CLI.
- `tailwind/input.css` — `@tailwind base/components/utilities` plus all custom CSS (animations, glass surfaces, prose overrides, Pygments tokens, admonitions). Edit this, not the rendered output.
- `custom_theme/assets/tailwind.css` — minified output. **Committed** to the repo so the site builds without running the CLI.
- `custom_theme/base.html` references it via `<link rel="stylesheet" href="{{ 'assets/tailwind.css'|url }}">`.

### Scheme de conectare Wokwi (`wiring/`)

Fiecare schemă de montaj e un folder `wiring/<nume>/` cu `diagram.json` (format Wokwi original, se poate lipi direct pe wokwi.com) și codul proiectului (`sketch.ino` / `main.py`). `uv run build` (sau `uv run build-diagrams`) randează piesele `@wokwi/elements@1.9.1` în Chromium headless și scrie `docs/assets/images/wiring/<nume>.svg`. SVG-urile sunt **commit-uite**: CI-ul nu are Chromium și sare pasul cu un avertisment.

```bash
uv sync --extra diagrams && uv run playwright install chromium   # o singură dată; pe macOS 13 se folosește Google Chrome instalat
uv run build-diagrams      # regenerează doar schemele cu diagram.json mai nou
uv run pytest              # teste pentru geometrie, SVG, hook
```

În pagină, pe un rând separat în secțiunea „Conectare”: `[[wokwi:<nume>]]` sau `[[wokwi:<nume>|<id-proiect-wokwi>]]` (adaugă butonul „Simulează în Wokwi”). `hooks/wokwi.py` îl transformă în figură; un nume inexistent pică build-ul. Pinii din `diagram.json` trebuie să coincidă cu tabelul „Conectare” al paginii. Traseele firelor urmează semantica Wokwi (vezi `specs/2026-10-15-wokwi-wiring-design.md`, „Traseele firelor”). Schemdraw (scheme electrice) doar cu aprobare explicită.

## Architecture

### Content pipeline

- `mkdocs.yml` is the single source of truth for site metadata and navigation. New pages must be added to `nav:` here **and** as a Markdown file under `docs/` — pages not in `nav` will not appear in the site chrome.
- `docs/` holds all published Markdown. Images live in `docs/assets/images/...` and are referenced with paths relative to the page (MkDocs copies them into the built site as-is).
- Per-page frontmatter (e.g. `category`, `tags`) is used by some project pages (see `docs/projects/arduino/led_cube.md`) — preserve the frontmatter shape when editing or adding sibling pages.

### Custom theme (`custom_theme/`)

The site does **not** use a stock MkDocs theme. `mkdocs.yml` sets `theme.name: null` and `theme.custom_dir: custom_theme`, so MkDocs renders every page through the templates in this directory.

- `custom_theme/base.html` — full HTML shell. All third-party assets are self-hosted from `custom_theme/assets/` (Tailwind bundle, Lucide icons, Inter + JetBrains Mono woff2). No external CDN/font requests at runtime. Exposes Jinja blocks `extrahead`, `content`, `extra_scripts`.

### Self-hosted assets (`custom_theme/assets/`)

Committed to the repo so the site has zero third-party requests for chrome/styling. Update procedure for each:

- `tailwind.css` — regenerated by `uv run build-css` (see Tailwind bundle section).
- `lucide.min.js` — Lucide icon library, pinned to v1.14.0 from `https://unpkg.com/lucide@1.14.0/dist/umd/lucide.min.js`. To bump: `curl -sL https://unpkg.com/lucide@<NEW>/dist/umd/lucide.min.js -o custom_theme/assets/lucide.min.js`.
- `fonts.css` + `fonts/*.woff2` — Inter (300/400/500/600/700) and JetBrains Mono (400/500), all subsets. To refresh, fetch the Google Fonts CSS with a Chrome User-Agent so it returns woff2 URLs:
  ```bash
  UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  curl -sLA "$UA" "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" \
    | sed 's|https://fonts.gstatic.com/[^)]*/\([^/)]*\.woff2\)|fonts/\1|g' > custom_theme/assets/fonts.css
  # Then download each woff2 referenced in fonts.css into custom_theme/assets/fonts/.
  ```
- `custom_theme/main.html` — extends `base.html`, implements `{% block content %}`. Branches on `page.is_homepage`: the homepage renders a custom hero/marketing layout and injects `{{ page.content }}` as the subtitle; all other pages render a standard article layout with `{{ page.title }}` and `{{ page.content }}` inside a Tailwind `prose` container.
- The top nav is generated by iterating `{% for nav_item in nav %}` in `base.html`, so nav labels/order come from `mkdocs.yml`'s `nav:` tree.
- Homepage status pill text is configurable via `extra.status_badge_text` and `extra.status_badge_highlight` in `mkdocs.yml`.

### `theme_template.html` (root)

A standalone design reference — the original full-page HTML mockup the custom theme was derived from. Not used at build time. When making visual changes, cross-reference this file to stay consistent with the intended design, but edit `custom_theme/` for anything that ships.

### `html/` (root)

Unrelated static HTML/CSS teaching samples (Bootstrap-based `home.html`, `reference.html`, `base_of_html.html`, `styles.css`) used as course material. Not part of the MkDocs build and not linked from `mkdocs.yml`.

## Conventions

- When adding a project page, place the Markdown under the matching `docs/projects/<platform>/` directory, add the entry to `nav:` in `mkdocs.yml`, and put images under `docs/assets/images/projects/<platform>/`.
- Site content is primarily in Romanian; keep new content in the same language as the surrounding section unless told otherwise.
