import re
import subprocess
import sys
from pathlib import Path


rst2kirlenthtml5 = Path(sys.executable).with_name("rst2kirlenthtml5")


def test_installation_should_create_console_script_for_html5_writer():
    assert rst2kirlenthtml5.exists()


def test_html5_writer_should_not_allow_xml_declaration_option(capfd):
    subprocess.run([kirlent2impressjs, "--xml-declaration"])
    captured = capfd.readouterr()
    assert "no such option: --xml-declaration" in captured.err


def test_html5_writer_should_not_allow_compact_lists_option(capfd):
    subprocess.run([kirlent2impressjs, "--compact-lists"])
    captured = capfd.readouterr()
    assert "no such option: --compact-lists" in captured.err


def test_html5_writer_should_not_allow_compact_field_lists_option(capfd):
    subprocess.run([kirlent2impressjs, "--compact-field-lists"])
    captured = capfd.readouterr()
    assert "no such option: --compact-field-lists" in captured.err


def test_html5_writer_should_not_allow_compact_table_style_option(capfd):
    subprocess.run([kirlent2impressjs, "--table-style"])
    captured = capfd.readouterr()
    assert "no such option: --table-style" in captured.err


def test_html5_writer_should_not_allow_compact_cloak_email_addresses_option(capfd):
    subprocess.run([kirlent2impressjs, "--cloak-email-addresses"])
    captured = capfd.readouterr()
    assert "no such option: --cloak-email-addresses" in captured.err


kirlent2impressjs = Path(sys.executable).with_name("kirlent2impressjs")


def test_installation_should_create_console_script_for_impressjs_writer():
    assert kirlent2impressjs.exists()


def test_impressjs_writer_should_embed_impressjs_stylesheet(capfd):
    subprocess.run([kirlent2impressjs])
    captured = capfd.readouterr()
    assert re.search(r"<style>.*\bimpress\b", captured.out, re.DOTALL)


def test_impressjs_writer_should_link_default_stylesheet_when_requested(capfd):
    subprocess.run([kirlent2impressjs, "--link-stylesheet"])
    captured = capfd.readouterr()
    assert re.search(
        r'<link rel="stylesheet" href=".*\bimpressjs.css"/>\n', captured.out
    )
