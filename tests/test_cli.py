import re
import subprocess
import sys
from pathlib import Path


rst2kirlenthtml5 = Path(sys.executable).with_name("rst2kirlenthtml5")


def test_installation_should_create_console_script_for_html5_writer():
    assert rst2kirlenthtml5.exists()


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
