# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Custom HTML5 writer for docutils.

This writer modifies the html5_polyglot writer in docutils.
The differences are:

- Uses "br" instead of line-block and line "div"s.
- Uses no "p" in single paragraph list items and table entries.
- Removes some docutils-specific classes.
"""

import re
from functools import partial
from pathlib import Path

from docutils import frontend
from docutils.writers.html5_polyglot import HTMLTranslator as HTML5Translator
from docutils.writers.html5_polyglot import Writer as HTML5Writer


class Writer(HTML5Writer):
    """Writer for generating HTML5 output."""

    supported = ("html", "html5")

    default_stylesheet_dirs = [".", str(Path(__file__).parent)] + \
        HTML5Writer.default_stylesheet_dirs[1:]

    settings_default_overrides = {
        "xml_declaration": False,
        "compact_lists": False,
        "compact_field_lists": False,
        "cloak_email_addresses": False,
    }

    settings_spec = frontend.filter_settings_spec(
        HTML5Writer.settings_spec,
        "xml_declaration",
        "no_xml_declaration",
        "compact_lists",
        "no_compact_lists",
        "compact_field_lists",
        "no_compact_field_lists",
        "cloak_email_addresses",
        stylesheet_dirs=(
            'Comma-separated list of directories where stylesheets are found. '
            'Used by --stylesheet-path when expanding relative path arguments. '
            '(default: "%s")' % ','.join(default_stylesheet_dirs),
            ['--stylesheet-dirs'],
            {
                'metavar': '<dir[,dir,...]>',
                'validator': frontend.validate_comma_separated_list,
                'default': default_stylesheet_dirs
            }
        ),
    )

    def __init__(self):
        super().__init__()
        self.translator_class = HTMLTranslator


class HTMLTranslator(HTML5Translator):
    """HTML5 translator for customizing generated output."""

    _remove_xml = partial(re.sub, re.compile(r'\s*\bxml(ns|:\w+)="[^"]*"'), '')
    _remove_type = partial(re.sub, re.compile(r'\s*\btype="[^"]*"'), '')

    head_prefix_template = _remove_xml(HTML5Translator.head_prefix_template)
    stylesheet_link = _remove_type(HTML5Translator.stylesheet_link)
    embedded_stylesheet = _remove_type(HTML5Translator.embedded_stylesheet)

    script = '<script%(mode)s>%(code)s</script>\n'
    script_external = '<script%(mode)s src="%(src)s"></script>\n'

    # no '<p>' under these if single paragraph
    SIMPLE_BLOCKS = {"definition", "entry", "field_body", "list_item"}

    UNWANTED_CLASSES = (
        ({"container"}, "container"),
        ({"container", "literal", "transition"}, "docutils"),
        ({"entry"}, "head"),
        ({"reference"}, "external"),
        ({"reference"}, "reference"),
    )

    def starttag(self, node, *args, **kwargs):
        # remove custom docutils classes
        classes = kwargs.pop("CLASS", "").split()
        classes.extend(kwargs.pop("class", "").split())
        classes.extend(kwargs.pop("classes", []))
        if len(classes) > 0:
            for tagnames, classname in HTMLTranslator.UNWANTED_CLASSES:
                if (node.tagname in tagnames) and (classname in classes):
                    classes.remove(classname)
            if len(classes) > 0:
                kwargs["CLASS"] = " ".join(classes)

        # add custom properties if any
        kwargs.update(node.attributes.pop("custom", {}))
        return super().starttag(node, *args, **kwargs)

    def is_compactable(self, *args, **kwargs):
        # suppress generation of "simple" classes for all elements
        return False

    def visit_paragraph(self, node):
        # suppress '<p>' in single paragraph simple blocks
        single_p = (len(node.parent.children) < 2) and \
            (node.parent.tagname in HTMLTranslator.SIMPLE_BLOCKS)
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
        self.body.append('<br/>\n')
