# Copyright 2020-2021 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Custom writers for docutils."""

__version__ = "0.1.0"

from docutils.core import publish_cmdline

from . import html5


def publish_cmdline_html5(*args, **kwargs):
    """Run utility for converting an RST file to HTML5."""
    publish_cmdline(*args, **kwargs, writer=html5.Writer())
