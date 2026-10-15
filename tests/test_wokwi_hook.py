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
