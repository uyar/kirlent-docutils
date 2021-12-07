# Copyright 2020-2021 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""impress.js writer for docutils."""

import re
from pathlib import Path

from . import html5
from .utils import modify_spec


IMPRESS_JS_URL = "https://impress.js.org/js/impress.js"
IMPRESS_JS_INIT = """
    window.addEventListener('DOMContentLoaded', function() {
        impress().init();
    }, false);
"""

ROUGH_NOTATION_URL = "https://unpkg.com/rough-notation/lib/rough-notation.iife.js"  # noqa
ROUGH_NOTATION_ANNOTATE = """
    function annotate(event, element, type) {
        event.preventDefault();
        const annotation = RoughNotation.annotate(element, {type: type});
        annotation.show();
    }
"""

ANNOTATION_PREFIX = "annotate://"
ANNOTATION_MARKUP = '<span onclick="annotate(event, this, \'%(type)s\')">'

DEFAULT_STEP_WIDTH, DEFAULT_STEP_HEIGHT = 1920, 1080
DEFAULT_STEP_DEPTH = 1000


class Writer(html5.Writer):
    """Writer for generating impress.js output."""

    default_stylesheets = ["impressjs.css"]
    default_stylesheet_dirs = [".", str(Path(__file__).parent)] + \
        html5.Writer.default_stylesheet_dirs[1:]

    settings_spec = (
        "impress.js-Specific Options",
        html5.Writer.settings_spec[1],
        modify_spec(
            html5.Writer.settings_spec,
            skip={},
            overrides={
                "--stylesheet-path": {
                    "options": {
                        "default": default_stylesheets,
                    },
                    "message_sub": (
                        re.compile(r'(.*\bDefault: )".*"$'),
                        '"%s"' % ",".join(default_stylesheets),
                    ),
                },
                "--stylesheet-dirs": {
                    "options": {
                        "default": default_stylesheet_dirs,
                    },
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
        self.translator_class = ImpressJSTranslator


class ImpressJSTranslator(html5.HTMLTranslator):
    """Translator for generating impress.js markup."""

    script_impressjs = html5.HTMLTranslator.script_external % {
        "mode": " defer",
        "src": IMPRESS_JS_URL,
    }

    script_impressjs_init = html5.HTMLTranslator.script % {
        "mode": "",
        "code": IMPRESS_JS_INIT,
    }

    script_rough_notation = html5.HTMLTranslator.script_external % {
        "mode": " defer",
        "src": ROUGH_NOTATION_URL,
    }

    script_rough_notation_annotate = html5.HTMLTranslator.script % {
        "mode": "",
        "code": ROUGH_NOTATION_ANNOTATE,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add attributes to keep track of the field data
        self.__fields = {}
        self.__field_name, self.__field_body = None, None

        # use a default horizontal step of one step width
        self.__fields["data-rel-x"] = str(DEFAULT_STEP_WIDTH)

    def visit_document(self, node):
        # add attributes for impress.js
        node.attributes["ids"].append("impress")
        node.attributes["custom"] = {
            "data-width": str(DEFAULT_STEP_WIDTH),
            "data-height": str(DEFAULT_STEP_HEIGHT),
        }
        super().visit_document(node)

        # note the title in order to add it to docinfo later
        self.title.append(node.get("title", ""))

    def depart_document(self, node):
        super().depart_document(node)

        # add code for impress.js
        self.head.append(ImpressJSTranslator.script_impressjs)
        self.head.append(ImpressJSTranslator.script_impressjs_init)

        # add code for loading rough notation
        self.head.append(ImpressJSTranslator.script_rough_notation)
        self.head.append(ImpressJSTranslator.script_rough_notation_annotate)

    def depart_docinfo(self, node):
        # wrap docinfo in a step with a title
        super().depart_docinfo(node)
        self.docinfo.insert(0, '<section class="step" id="docinfo">\n')
        self.docinfo.insert(1, '<h1>%(t)s</h1>\n' % {"t": self.title[0]})
        self.docinfo.append('</section>\n')

    def visit_transition(self, node):
        # suppress '<hr/>'
        pass

    def visit_field_list(self, node):
        # suppress '<dl>'
        pass

    def depart_field_list(self, node):
        pass

    def visit_field_name(self, node):
        # suppress '<dt>'
        pass

    def depart_field_name(self, node):
        pass

    def visit_field_body(self, node):
        # suppress '<dd>'
        pass

    def depart_field_body(self, node):
        # store field name and value in fields
        self.__fields[self.__field_name] = self.__field_body
        self.__field_name, self.__field_body = None, None

    def visit_Text(self, node):
        # suppress text generation under field names and bodies
        parent = node.parent
        if parent.tagname == "field_name":
            self.__field_name = node.astext()
        elif parent.parent.tagname == "field_body":
            self.__field_body = node.astext()
        else:
            super().visit_Text(node)

    def visit_section(self, node):
        # start a step
        node.attributes["classes"].insert(0, "step")
        node.attributes["custom"] = self.__fields
        super().visit_section(node)
        self.__fields = {}

    def visit_reference(self, node):
        # generate '<span>' for annotation
        refuri = node.get("refuri", "")
        annotation = refuri.startswith(ANNOTATION_PREFIX)
        if not annotation:
            super().visit_reference(node)
        else:
            annotation_type = refuri[len(ANNOTATION_PREFIX):]
            self.body.append(ANNOTATION_MARKUP % {"type": annotation_type})
        node.attributes["_annotation"] = annotation

    def depart_reference(self, node):
        annotation = node.attributes.pop("_annotation", False)
        if not annotation:
            super().depart_reference(node)
        else:
            self.body.append('</span>')
