import re
import subprocess
import sys
from pathlib import Path


rst2kirlenthtml5 = Path(sys.executable).with_name("rst2kirlenthtml5")


def test_installation_should_create_console_script_for_html5_writer():
    assert rst2kirlenthtml5.exists()


def test_html5_writer_should_not_allow_xml_declaration_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--xml-declaration", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --xml-declaration" in captured.err


def test_html5_writer_should_not_allow_no_xml_declaration_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--no-xml-declaration", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --no-xml-declaration" in captured.err


def test_html5_writer_should_not_allow_compact_lists_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--compact-lists", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --compact-lists" in captured.err


def test_html5_writer_should_not_allow_no_compact_lists_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--no-compact-lists", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --no-compact-lists" in captured.err


def test_html5_writer_should_not_allow_compact_field_lists_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--compact-field-lists", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --compact-field-lists" in captured.err


def test_html5_writer_should_not_allow_no_compact_field_lists_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--no-compact-field-lists", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --no-compact-field-lists" in captured.err


def test_html5_writer_should_include_kirlent_minimal_stylesheet(capfd):
    subprocess.run([rst2kirlenthtml5, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent minimal stylesheet for HTML5" in captured.out


kirlent2impressjs = Path(sys.executable).with_name("kirlent2impressjs")


def test_installation_should_create_console_script_for_impressjs_writer():
    assert kirlent2impressjs.exists()


def test_impressjs_writer_should_include_kirlent_minimal_stylesheet(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent minimal stylesheet for HTML5" in captured.out


def test_impressjs_writer_should_include_kirlent_minimal_impressjs_stylesheet(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent minimal stylesheet for impress.js" in captured.out


def test_impressjs_writer_should_use_default_slide_size_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-height="1080".*data-width="1920".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_given_slide_size_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=42x35", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-height="35".*data-width="42".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_given_standard_size_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=a4", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-height="795".*data-width="1125".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_default_transition_duration_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-transition-duration="1000".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_given_transition_duration_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--transition-duration=7", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-transition-duration="7".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_default_min_scale_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-min-scale="0".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_given_min_scale_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--min-scale=1", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-min-scale="1".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_default_max_scale_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-max-scale="3".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_given_max_scale_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--max-scale=2", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'data-max-scale="2".*id="impress"', captured.out) is not None


def test_impressjs_writer_should_use_default_slide_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'.step {\s+width: 1920px;\s+height: 1080px;', captured.out) is not None


def test_impressjs_writer_should_use_given_slide_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=42x35", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'.step {\s+width: 42px;\s+height: 35px;', captured.out) is not None


def test_impressjs_writer_should_use_given_standard_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=a4", "/dev/null"])
    captured = capfd.readouterr()
    assert re.search(r'.step {\s+width: 1125px;\s+height: 795px;', captured.out) is not None


def test_impressjs_writer_should_use_default_font_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert 'font-size: 45px;' in captured.out


def test_impressjs_writer_should_use_automatic_font_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=1024x768", "/dev/null"])
    captured = capfd.readouterr()
    assert 'font-size: 25px;' in captured.out


def test_impressjs_writer_should_use_given_font_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--font-size=3", "/dev/null"])
    captured = capfd.readouterr()
    assert 'font-size: 3px;' in captured.out
