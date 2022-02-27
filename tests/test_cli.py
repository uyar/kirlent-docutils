import re
import subprocess
import sys
from functools import partial
from pathlib import Path


compact = partial(re.sub, re.compile(r'\s+'), ' ')


rst2kirlenthtml5 = Path(sys.executable).with_name("rst2kirlenthtml5")


def test_installation_should_create_console_script_for_html5_writer():
    assert rst2kirlenthtml5.exists()


def test_html5_writer_should_not_allow_xml_declaration_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--xml-declaration", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --xml-declaration" in captured.err


def test_html5_writer_should_not_allow_compact_lists_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--compact-lists", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --compact-lists" in captured.err


def test_html5_writer_should_not_allow_compact_field_lists_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--compact-field-lists", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --compact-field-lists" in captured.err


def test_html5_writer_should_not_allow_cloak_email_addresses_option(capfd):
    subprocess.run([rst2kirlenthtml5, "--cloak-email-addresses", "/dev/null"])
    captured = capfd.readouterr()
    assert "no such option: --cloak-email-addresses" in captured.err


def test_html5_writer_should_include_kirlent_minimal_stylesheet(capfd):
    subprocess.run([rst2kirlenthtml5, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent minimal stylesheet" in captured.out


def test_html5_writer_should_include_kirlent_plain_stylesheet(capfd):
    subprocess.run([rst2kirlenthtml5, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent plain stylesheet" in captured.out


kirlent2impressjs = Path(sys.executable).with_name("kirlent2impressjs")


def test_installation_should_create_console_script_for_impressjs_writer():
    assert kirlent2impressjs.exists()


def test_impressjs_writer_should_include_kirlent_minimal_stylesheet(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent minimal stylesheet" in captured.out


def test_impressjs_writer_should_not_include_plain_stylesheet(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert "plain" not in captured.out


def test_impressjs_writer_should_include_kirlent_impressjs_stylesheet(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert "Kirlent stylesheet for impress.js" in captured.out


def test_impressjs_writer_should_use_default_slide_size_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert 'data-height="1080" data-width="1920" id="impress"' in captured.out


def test_impressjs_writer_should_use_given_slide_size_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=42x35", "/dev/null"])
    captured = capfd.readouterr()
    assert 'data-height="35" data-width="42" id="impress"' in captured.out


def test_impressjs_writer_should_use_given_standard_size_on_impress_element(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=a4", "/dev/null"])
    captured = capfd.readouterr()
    assert 'data-height="795" data-width="1125" id="impress"' in captured.out


def test_impressjs_writer_should_use_default_slide_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert '.step { width: 1920px; height: 1080px;' in compact(captured.out)


def test_impressjs_writer_should_use_given_slide_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=42x35", "/dev/null"])
    captured = capfd.readouterr()
    assert '.step { width: 42px; height: 35px;' in compact(captured.out)


def test_impressjs_writer_should_use_given_standard_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--slide-size=a4", "/dev/null"])
    captured = capfd.readouterr()
    assert '.step { width: 1125px; height: 795px;' in compact(captured.out)


def test_impressjs_writer_should_use_default_font_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "/dev/null"])
    captured = capfd.readouterr()
    assert 'font-size: 45px;' in compact(captured.out)


def test_impressjs_writer_should_use_given_font_size_on_step_style(capfd):
    subprocess.run([kirlent2impressjs, "--font-size=3", "/dev/null"])
    captured = capfd.readouterr()
    assert 'font-size: 3px;' in compact(captured.out)
