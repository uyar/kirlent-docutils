# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Custom writers for docutils."""

__version__ = "0.1.2"

from docutils.core import publish_cmdline

from . import html5, impressjs, revealjs, slides


def publish_cmdline_html5(*args, **kwargs):
    """Run utility for converting an RST file to HTML5."""
    publish_cmdline(*args, **kwargs, writer=html5.Writer())


def publish_cmdline_slides(*args, **kwargs):
    """Run utility for converting an RST file to an HTML5 presentation."""
    publish_cmdline(*args, **kwargs, writer=slides.Writer())


def publish_cmdline_impressjs(*args, **kwargs):
    """Run utility for converting an RST file to an impress.js presentation."""
    publish_cmdline(*args, **kwargs, writer=impressjs.Writer())


def publish_cmdline_revealjs(*args, **kwargs):
    """Run utility for converting an RST file to a reveal.js presentation."""
    publish_cmdline(*args, **kwargs, writer=revealjs.Writer())
