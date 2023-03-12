import pytest

import re
import subprocess
import sys
from pathlib import Path


def execute(tool, *args, content=""):
    echo = subprocess.Popen(
        [sys.executable, "-c", f"print('{content}')"],
        stdout=subprocess.PIPE,
    )
    subprocess.run([tool] + list(args), stdin=echo.stdout)


rst2kirlenthtml5 = Path(sys.executable).with_name("rst2kirlenthtml5")


def test_installation_should_create_console_script_for_html5_writer():
    assert rst2kirlenthtml5.exists()


@pytest.mark.parametrize(
    "option", [
        "--xml-declaration",
        "--no-xml-declaration",
        "--compact-lists",
        "--no-compact-lists",
        "--compact-field-lists",
        "--no-compact-field-lists",
        "--table-style",
    ])
def test_html5_writer_should_not_allow_removed_option(capfd, option):
    execute(rst2kirlenthtml5, option, content="")
    captured = capfd.readouterr()
    assert f"no such option: {option}" in captured.err


@pytest.mark.parametrize(
    ("sheet", "output"), [
        ("minimal", "HTML5"),
        ("plain", "HTML5"),
    ])
def test_html5_writer_should_include_html5_stylesheet(capfd, sheet, output):
    execute(rst2kirlenthtml5, content="")
    captured = capfd.readouterr()
    assert f"Kirlent {sheet} stylesheet for {output}" in captured.out


def test_html5_writer_should_include_bundled_mathjax_as_fallback(capfd):
    execute(rst2kirlenthtml5, "--math-output=mathjax", content=":math:`x_2`")
    captured = capfd.readouterr()
    assert str(Path("bundled/MathJax.min.js")) in captured.out


kirlent2slides = Path(sys.executable).with_name("kirlent2slides")


def test_installation_should_create_console_script_for_slides_writer():
    assert kirlent2slides.exists()


@pytest.mark.parametrize(
    ("sheet", "output"), [
        ("minimal", "HTML5"),
        ("plain", "HTML5"),
        ("base", "slides"),
        ("simple", "slides"),
    ])
def test_slides_writer_should_include_slides_stylesheet(capfd, sheet, output):
    execute(kirlent2slides, content="")
    captured = capfd.readouterr()
    assert f"Kirlent {sheet} stylesheet for {output}" in captured.out


kirlent2impressjs = Path(sys.executable).with_name("kirlent2impressjs")


def test_installation_should_create_console_script_for_impressjs_writer():
    assert kirlent2impressjs.exists()


@pytest.mark.parametrize(
    ("sheet", "output"), [
        ("minimal", "HTML5"),
        ("plain", "HTML5"),
        ("base", "slides"),
        ("base", "impress.js"),
    ])
def test_impressjs_writer_should_include_impressjs_stylesheet(capfd, sheet, output):
    execute(kirlent2impressjs, content="")
    captured = capfd.readouterr()
    assert f"Kirlent {sheet} stylesheet for {output}" in captured.out


@pytest.mark.parametrize(
    ("size", "width", "height"), [
        (None, "1920", "1080"),
        ("42x35", "42", "35"),
        ("a4", "1125", "795"),
    ]
)
def test_impressjs_writer_should_set_slide_size_on_step_style(capfd, size, width, height):
    if size is None:
        execute(kirlent2impressjs, content="")
    else:
        execute(kirlent2impressjs, f"--slide-size={size}", content="")
    captured = capfd.readouterr()
    assert re.search(
        fr'<style>\s*\.step {{\s*width: {width}px;\s*height: {height}px;\s*}}\s*</style>',
        captured.out,
    ) is not None


@pytest.mark.parametrize(
    ("size", "width", "height"), [
        (None, "1920", "1080"),
        ("42x35", "42", "35"),
        ("a4", "1125", "795"),
    ]
)
def test_impressjs_writer_should_set_slide_size_on_impress_element(capfd, size, width, height):
    if size is None:
        execute(kirlent2impressjs, content="")
    else:
        execute(kirlent2impressjs, f"--slide-size={size}", content="")
    captured = capfd.readouterr()
    assert re.search(
        fr'\bdata-height="{height}"[^>]*\bdata-width="{width}"[^>]*\bid="impress"',
        captured.out,
    ) is not None


@pytest.mark.parametrize(
    ("attr", "option", "value"), [
        ("transition-duration", None, "1000"),
        ("transition-duration", "0", "0"),
        ("min-scale", None, "0"),
        ("min-scale", "1", "1"),
        ("max-scale", None, "3"),
        ("max-scale", "2", "2"),
    ]
)
def test_impressjs_writer_should_set_data_attr_on_impress_element(capfd, attr, option, value):
    if option is None:
        execute(kirlent2impressjs, content="")
    else:
        execute(kirlent2impressjs, f"--{attr}={option}", content="")
    captured = capfd.readouterr()
    assert re.search(
        fr'\bdata-{attr}="{value}"[^>]*\bid="impress"',
        captured.out,
    ) is not None


kirlent2revealjs = Path(sys.executable).with_name("kirlent2revealjs")


def test_installation_should_create_console_script_for_revealjs_writer():
    assert kirlent2revealjs.exists()


@pytest.mark.parametrize(
    ("sheet", "output"), [
        ("minimal", "HTML5"),
        ("plain", "HTML5"),
        ("base", "slides"),
        ("base", "reveal.js"),
    ])
def test_revealjs_writer_should_include_revealjs_stylesheet(capfd, sheet, output):
    execute(kirlent2revealjs, content="")
    captured = capfd.readouterr()
    assert f"Kirlent {sheet} stylesheet for {output}" in captured.out


def test_revealjs_writer_should_activate_notes_plugin_on_initialization(capfd):
    execute(kirlent2revealjs, content="")
    captured = capfd.readouterr()
    assert re.search(
        r"Reveal.initialize\({(\s*.*,)*\s*plugins: \[RevealNotes\]",
        captured.out,
    ) is not None


@pytest.mark.parametrize(
    ("size", "width", "height"), [
        (None, "1920", "1080"),
        ("42x35", "42", "35"),
        ("a4", "1125", "795"),
    ]
)
def test_revealjs_writer_should_set_slide_size_on_initialization(capfd, size, width, height):
    if size is None:
        execute(kirlent2revealjs, content="")
    else:
        execute(kirlent2revealjs, f"--slide-size={size}", content="")
    captured = capfd.readouterr()
    assert re.search(
        fr"Reveal.initialize\({{(\s*.*,)*\s*width: {width},\s*height: {height}",
        captured.out,
    ) is not None


REVEALJS_ATTRS = {
    "min-scale": "minScale",
    "max-scale": "maxScale",
    "center-vertical": "center",
}


@pytest.mark.parametrize(
    ("attr", "option", "value"), [
        ("min-scale", None, "0"),
        ("min-scale", "1", "1"),
        ("max-scale", None, "3"),
        ("max-scale", "2", "2"),
        ("transition", None, "none"),
        ("transition", "concave", "concave"),
        ("center-vertical", None, "false"),
        ("center-vertical", "true", "true"),
    ]
)
def test_revealjs_writer_should_set_attr_on_initialization(capfd, attr, option, value):
    if option is None:
        execute(kirlent2revealjs, content="")
    else:
        execute(kirlent2revealjs, f"--{attr}={option}", content="")
    captured = capfd.readouterr()
    attr_name = REVEALJS_ATTRS.get(attr, attr)
    attr_value = f"'{value}'" if attr == "transition" else f"{value}"
    assert re.search(
        fr"Reveal.initialize\({{(\s*.*,)*\s*{attr_name}: {attr_value}",
        captured.out,
    ) is not None
