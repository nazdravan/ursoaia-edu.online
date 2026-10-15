"""Console-script wrappers so `uv run serve` / `uv run build` invoke mkdocs.

`build_css` compiles Tailwind via the standalone CLI; `build_images` writes a
.webp sibling next to every raster image under docs/. `serve` and `build` run
both first so the bundled stylesheet and WebP variants are fresh before MkDocs
copies them into the site. `build_diagrams` renders Wokwi wiring diagrams
from `wiring/*/diagram.json` into `docs/assets/images/wiring/*.svg`.
"""
from __future__ import annotations

import os
import platform
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path

from mkdocs.__main__ import cli

TAILWIND_VERSION = "v3.4.17"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TAILWIND_DIR = PROJECT_ROOT / "tailwind"
TAILWIND_BIN = TAILWIND_DIR / "bin" / "tailwindcss"
TAILWIND_CONFIG = TAILWIND_DIR / "tailwind.config.js"
TAILWIND_INPUT = TAILWIND_DIR / "input.css"
TAILWIND_OUTPUT = PROJECT_ROOT / "custom_theme" / "assets" / "tailwind.css"

DOCS_DIR = PROJECT_ROOT / "docs"
WEBP_QUALITY = 80
RASTER_EXTS = {".jpg", ".jpeg", ".png"}
WIRING_DIR = PROJECT_ROOT / "wiring"
WIRING_OUT = DOCS_DIR / "assets" / "images" / "wiring"
WOKWI_BUNDLE = PROJECT_ROOT / "tools" / "wokwi" / "wokwi-elements.bundle.js"


def _tailwind_asset() -> str:
    machine = platform.machine().lower()
    system = platform.system().lower()
    if system == "linux":
        return "tailwindcss-linux-x64" if machine in {"x86_64", "amd64"} else "tailwindcss-linux-arm64"
    if system == "darwin":
        return "tailwindcss-macos-arm64" if machine in {"arm64", "aarch64"} else "tailwindcss-macos-x64"
    if system == "windows":
        return "tailwindcss-windows-x64.exe"
    raise RuntimeError(f"Unsupported platform: {system}/{machine}")


def _ensure_binary() -> Path:
    if TAILWIND_BIN.exists():
        return TAILWIND_BIN
    TAILWIND_BIN.parent.mkdir(parents=True, exist_ok=True)
    asset = _tailwind_asset()
    url = f"https://github.com/tailwindlabs/tailwindcss/releases/download/{TAILWIND_VERSION}/{asset}"
    print(f"Downloading Tailwind CLI {TAILWIND_VERSION} ({asset})...", file=sys.stderr)
    urllib.request.urlretrieve(url, TAILWIND_BIN)  # noqa: S310 — pinned vendor URL
    TAILWIND_BIN.chmod(TAILWIND_BIN.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return TAILWIND_BIN


def build_css() -> None:
    binary = _ensure_binary()
    cmd = [
        str(binary),
        "-c", str(TAILWIND_CONFIG),
        "-i", str(TAILWIND_INPUT),
        "-o", str(TAILWIND_OUTPUT),
        "--minify",
    ]
    if "--watch" in sys.argv[1:]:
        cmd.append("--watch")
    TAILWIND_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, cwd=PROJECT_ROOT, check=True)


def build_images() -> None:
    """Generate .webp siblings for every raster image under docs/.

    Skips images whose .webp is newer than the source. Drops alpha by
    flattening PNGs onto white before encoding so we always get the smallest
    lossy WebP.
    """
    from PIL import Image

    converted = 0
    skipped = 0
    for src in DOCS_DIR.rglob("*"):
        if src.suffix.lower() not in RASTER_EXTS or not src.is_file():
            continue
        dst = src.with_suffix(".webp")
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            skipped += 1
            continue
        with Image.open(src) as img:
            if img.mode in ("RGBA", "LA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            img.save(dst, "WEBP", quality=WEBP_QUALITY, method=6)
        converted += 1
    print(f"WebP: converted {converted}, skipped {skipped} (up-to-date)", file=sys.stderr)


def build_diagrams() -> None:
    """Regenerează SVG-urile Wokwi din wiring/*/diagram.json (vezi wiring.py)."""
    from ursoaia_edu_online.wiring import render_all

    render_all(WIRING_DIR, WIRING_OUT, WOKWI_BUNDLE)


def serve() -> None:
    if os.environ.get("URSOAIA_SKIP_CSS") != "1":
        build_css()
    if os.environ.get("URSOAIA_SKIP_IMAGES") != "1":
        build_images()
    if os.environ.get("URSOAIA_SKIP_DIAGRAMS") != "1":
        build_diagrams()
    cli.main(args=["serve", *sys.argv[1:]], prog_name="uv run serve", standalone_mode=True)


def build() -> None:
    if os.environ.get("URSOAIA_SKIP_CSS") != "1":
        build_css()
    if os.environ.get("URSOAIA_SKIP_IMAGES") != "1":
        build_images()
    if os.environ.get("URSOAIA_SKIP_DIAGRAMS") != "1":
        build_diagrams()
    cli.main(args=["build", *sys.argv[1:]], prog_name="uv run build", standalone_mode=True)
