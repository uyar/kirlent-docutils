# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Custom HTML5 writer for docutils.

This writer modifies the html5_polyglot writer.
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

from .utils import stylesheet_dirs_option, stylesheet_path_option


class Writer(HTML5Writer):
    """Writer for generating HTML5 output."""

    supported = ("html", "html5")

    default_stylesheets = ["kirlent_html5.css"]

    default_stylesheet_dirs = [".", str(Path(__file__).parent)] + \
        HTML5Writer.default_stylesheet_dirs[1:]

    settings_default_overrides = {
        "xml_declaration": False,
        "compact_lists": False,
        "compact_field_lists": False,
        "table_style": "colwidths-auto",
    }

    settings_spec = frontend.filter_settings_spec(
        HTML5Writer.settings_spec,
        "xml_declaration",
        "no_xml_declaration",
        "compact_lists",
        "no_compact_lists",
        "compact_field_lists",
        "no_compact_field_lists",
        "table_style",
        stylesheet_path=stylesheet_path_option(default_stylesheets),
        stylesheet_dirs=stylesheet_dirs_option(default_stylesheet_dirs),
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

    script = '<script>%(code)s</script>\n'
    script_external = '<script src="%(src)s"></script>\n'
    script_defer = '<script defer src="%(src)s"></script>\n'

    mathjax_script = _remove_type(HTML5Translator.mathjax_script)
    mathjax_url = "file://%(path)s" % {
        "path": Path(__file__).parent / "bundled" / "MathJax.min.js",
    }

    # no '<p>' under these if single paragraph
    SIMPLE_BLOCKS = {"definition", "entry", "field_body", "list_item"}

    UNWANTED_CLASSES = {
        "container": {"container", "docutils"},
        "entry": {"head"},
        "literal": {"docutils"},
        "literal_block": {"literal-block"},
        "reference": {"external", "internal", "reference"},
        "target": {"target"},
        "title": {"title"},
        "transition": {"docutils"},
    }

    COLON_SPAN = '<span class="colon">:</span>'

    def starttag(self, node, *args, **kwargs):
        # remove custom docutils classes
        classes = kwargs.pop("CLASS", "").split()
        classes.extend(kwargs.pop("class", "").split())
        classes.extend(kwargs.pop("classes", []))
        if len(classes) > 0:
            unwanted = HTMLTranslator.UNWANTED_CLASSES.get(node.tagname, set())
            to_remove = [c for c in classes if c in unwanted]
            for classname in to_remove:
                classes.remove(classname)
            if len(classes) > 0:
                kwargs["CLASS"] = " ".join(classes)

        # add custom styles and properties, if any
        custom = node.attributes.pop("_custom", {})
        styles = node.attributes.pop("_styles", {})
        if len(styles) > 0:
            custom["style"] = " ".join(f"{k}: {v};" for k, v in styles.items())
        kwargs.update(custom)
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

    def visit_docinfo_item(self, node, *args, **kwargs):
        # suppress '<span class="colon">'
        super().visit_docinfo_item(node, *args, **kwargs)
        self.body[-2] = self.body[-2].replace(HTMLTranslator.COLON_SPAN, ':')

    def depart_field_name(self, node):
        # suppress '<span class="colon">'
        self.body[-1] = self.body[-1].replace(HTMLTranslator.COLON_SPAN, ':')
