import re
import subprocess
import sys
from pathlib import Path


rst2kirlenthtml5 = Path(sys.executable).with_name("rst2kirlenthtml5")


def test_installation_should_create_console_script_for_html5_writer():
    assert rst2kirlenthtml5.exists()


def test_html5_writer_should_embed_default_stylesheet(capfd):
    subprocess.run([rst2kirlenthtml5])
    captured = capfd.readouterr()
    assert re.search(
        r"<style>.*\bMinimal\b.*\bKirlent-HTML\b.*</style>\n", captured.out, re.DOTALL
    )


def test_html5_writer_should_link_default_stylesheet_when_requested(capfd):
    subprocess.run([rst2kirlenthtml5, "--link-stylesheet"])
    captured = capfd.readouterr()
    assert re.search(
        r'<link rel="stylesheet" href=".*/kirlent_minimal.css"/>\n', captured.out
    )
