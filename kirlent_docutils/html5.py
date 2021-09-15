# Copyright 2020-2021 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Custom HTML5 writer for docutils.

This writer modifies the html5_polyglot writer in docutils.
The differences are:

- No classes other than user-defined classes.
- No space before the slash at the end of self-closing tags.
- "main" and "section" elements instead of "div" elements.
- "br" elements instead of line block "div" elements.
- No "p" elements in single paragraph list items and table entries.
"""

import re
from functools import partial
from pathlib import Path

from docutils.writers.html5_polyglot import HTMLTranslator as HTML5Translator
from docutils.writers.html5_polyglot import Writer as HTML5Writer

from .utils import modify_spec


class Writer(HTML5Writer):
    """Writer for generating HTML5 output."""

    supported = ("html", "html5")

    default_stylesheets = ["kirlent_minimal.css"]
    default_stylesheet_dirs = [".", str(Path(__file__).parent)]

    settings_default_overrides = {
        "xml_declaration": False,
        "compact_lists": False,
        "compact_field_lists": False,
        "table_style": "colwidths-auto",
        "cloak_email_addresses": False,
    }

    settings_spec = (
        "Kirlent HTML5-Specific Options",
        HTML5Writer.settings_spec[1],
        modify_spec(
            HTML5Writer.settings_spec,
            skip={
                "--xml-declaration",
                "--no-xml-declaration",
                "--compact-lists",
                "--no-compact-lists",
                "--compact-field-lists",
                "--no-compact-field-lists",
                "--table-style",
                "--cloak-email-addresses",
            },
            overrides={
                "--stylesheet-path": {
                    "options": {"default": default_stylesheets},
                    "message_sub": (
                        re.compile(r'(.*\bDefault: )".*"$'),
                        '"%s"' % ",".join(default_stylesheets),
                    ),
                },
                "--stylesheet-dirs": {
                    "options": {"default": default_stylesheet_dirs},
                    "message_sub": (
                        re.compile(r'(.*\bDefault: )".*"$'),
                        '"%s"' % ",".join(default_stylesheet_dirs),
                    ),
                },
            },
        ),
    )

    def __init__(self):
        super().__init__()
        self.translator_class = HTMLTranslator


class HTMLTranslator(HTML5Translator):
    """HTML5 translator for customizing generated output."""

    _remove_closing_space = partial(re.sub, re.compile(r"\s+/>$"), "/>")
    _remove_xml = partial(re.sub, re.compile(r'\s*\bxml(ns|:\w+)="[^"]*"'), "")
    _remove_type = partial(re.sub, re.compile(r'\s*\btype="[^"]*"'), "")
    _remove_class = partial(re.sub, re.compile(r'(\s*\bclass="[^"]*")'), "")

    head_prefix_template = _remove_xml(HTML5Translator.head_prefix_template)
    content_type = _remove_closing_space(HTML5Translator.content_type)
    generator = _remove_closing_space(HTML5Translator.generator)
    stylesheet_link = _remove_closing_space(
        _remove_type(HTML5Translator.stylesheet_link)
    )
    embedded_stylesheet = _remove_type(HTML5Translator.embedded_stylesheet)

    # no '<p>' under these if single paragraph
    SIMPLE_BLOCKS = {"definition", "entry", "field_body", "list_item"}

    def starttag(self, *args, **kwargs):
        # remove custom docutils classes
        _ = kwargs.pop("CLASS", None)
        return super().starttag(*args, **kwargs)

    def emptytag(self, *args, **kwargs):
        tag = super().emptytag(*args, **kwargs)

        # remove space before closing slash
        return HTMLTranslator._remove_closing_space(tag)

    def visit_docinfo_item(self, node, name, meta=True):
        super().visit_docinfo_item(node, name, meta=meta)

        # for '<meta/>' tags, remove space before closing slash
        if meta:
            tag = HTMLTranslator._remove_closing_space(self.meta[-1])
            self.meta[-1] = self.head[-1] = tag

    def depart_document(self, node):
        prefix_size, suffix_size = len(self.body_prefix), len(self.body_suffix)

        super().depart_document(node)

        # replace '<div class="document">' with '<main>'
        tag = self.starttag(node, "main")
        self.body_prefix[-1] = self.html_body[prefix_size - 1] = tag
        self.body_suffix[0] = self.html_body[-suffix_size] = "</main>\n"

    def visit_section(self, node):
        super().visit_section(node)

        # replace '<div class="section">' with '<section>'
        self.body[-1] = self.starttag(node, "section")

    def depart_section(self, node):
        super().depart_section(node)
        self.body[-1] = "</section>\n"

    def visit_paragraph(self, node):
        # suppress '<p>' in single paragraph simple blocks
        single_p = (len(node.parent.children) < 2) and (
            node.parent.tagname in HTMLTranslator.SIMPLE_BLOCKS
        )
        if not single_p:
            super().visit_paragraph(node)
        node.attributes["_single_p"] = single_p

    def depart_paragraph(self, node):
        single_p = node.attributes.pop("_single_p", False)
        if not single_p:
            super().depart_paragraph(node)

    def visit_line_block(self, node):
        # suppress '<div class="line-block">'
        pass

    def depart_line_block(self, node):
        pass

    def visit_line(self, node):
        # suppress '<div class="line">'
        pass

    def depart_line(self, node):
        # add '<br/>' to end of line
        self.body.append("<br/>\n")

    def visit_reference(self, node):
        # remove custom classes in anchors
        href = node["refuri"] if "refuri" in node else "#" + node["refid"]
        self.body.append(self.starttag(node, "a", "", href=href))

    def visit_entry(self, node):
        super().visit_entry(node)

        # remove all classes in table entries
        self.body[-1] = HTMLTranslator._remove_class(self.body[-1])
