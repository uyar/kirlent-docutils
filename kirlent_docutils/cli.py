# Copyright 2020-2023 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent-docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Command-line entry points for Kırlent writers."""

from docutils.core import publish_cmdline

from . import html5, impressjs, revealjs, slides


def publish_cmdline_html5(*args, **kwargs):
    """Convert RST to HTML5."""
    publish_cmdline(*args, **kwargs, writer=html5.Writer())


def publish_cmdline_slides(*args, **kwargs):
    """Convert RST to HTML5-based slides."""
    publish_cmdline(*args, **kwargs, writer=slides.Writer())


def publish_cmdline_impressjs(*args, **kwargs):
    """Convert RST to impress.js presentation."""
    publish_cmdline(*args, **kwargs, writer=impressjs.Writer())


def publish_cmdline_revealjs(*args, **kwargs):
    """Convert RST to reveal.js presentation."""
    publish_cmdline(*args, **kwargs, writer=revealjs.Writer())
