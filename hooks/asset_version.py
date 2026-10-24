"""MkDocs hook: cache-busting for the theme's own CSS/JS.

GitHub Pages serves `assets/*` with `cache-control: max-age=604800`, so after a
deploy browsers keep the old `tailwind.css` for up to a week and new utility
classes silently do nothing. This hook registers a Jinja filter `versioned`
that appends `?v=<content hash>` to a theme asset path; the URL changes only
when the file itself changes.

Usage in templates: `{{ 'assets/tailwind.css'|versioned|url }}`.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

_THEME_DIR = Path(__file__).resolve().parent.parent / "custom_theme"


def _versioned(path: str) -> str:
    file = _THEME_DIR / path
    if not file.is_file():
        return path
    digest = hashlib.sha256(file.read_bytes()).hexdigest()[:10]
    return f"{path}?v={digest}"


def on_env(env, config, files):
    env.filters["versioned"] = _versioned
    return env
