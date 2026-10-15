import json
import os
import sys
import time
import xml.etree.ElementTree as ET

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
            wiring._launch_browser(p).close()
    except Exception:
        pytest.skip("Chromium nu e instalat (uv run playwright install chromium)")
    wiring_dir, out_dir = _write(tmp_path)
    bundle = wiring.ensure_bundle(tmp_path / "bundle.js")
    assert wiring.render_all(wiring_dir, out_dir, bundle) == 1
    svg = (out_dir / "led.svg").read_text("utf-8")
    assert svg.startswith("<svg ") and 'stroke="green"' in svg and '<g id="p-uno"' in svg
    ET.fromstring(svg)  # <img src=*.svg> e parsat ca XML: entitățile HTML (&nbsp;) îl strică
    assert wiring.render_all(wiring_dir, out_dir, bundle) == 0  # la zi


class _FakeChromium:
    def __init__(self, ok_channel):
        self.ok_channel, self.calls = ok_channel, []

    def launch(self, **kw):
        self.calls.append(kw.get("channel"))
        if kw.get("channel") != self.ok_channel:
            raise RuntimeError("not available")
        return "browser"


class _FakePlaywright:
    def __init__(self, ok_channel):
        self.chromium = _FakeChromium(ok_channel)


def test_launch_browser_falls_back_to_installed_chrome():
    # Playwright nu are Chromium propriu pe macOS 13; Google Chrome instalat trebuie folosit
    fake = _FakePlaywright("chrome")
    assert wiring._launch_browser(fake) == "browser"
    assert fake.chromium.calls == [None, "chrome"]


def test_launch_browser_raises_when_nothing_available():
    fake = _FakePlaywright("none")
    with pytest.raises(RuntimeError):
        wiring._launch_browser(fake)
