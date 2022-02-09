# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""impress.js writer for docutils."""

from docutils import frontend

from .html5 import HTMLTranslator
from .html5 import Writer as HTMLWriter


IMPRESS_JS_URL = "https://impress.js.org/js/impress.js"

IMPRESS_JS_INIT = """
  window.addEventListener('DOMContentLoaded', () => {
      impress().init();
  }, false);
"""

IMPRESS_JS_STYLE = """
  .step {
    width: %(width)dpx;
    height: %(height)dpx;
    font-size: %(font_size)s;
  }
"""

IMPRESS_JS_ATTRS = {
    "data-x", "data-y", "data-z",
    "data-rel-x", "data-rel-y", "data-rel-z",
    "data-rotate-x", "data-rotate-y", "data-rotate-z",
    "data-rotate", "data-rotate-order",
    "data-scale",
}

ANNOTATION_PREFIX = "annotate://"

ANNOTATION_COLOR_PROPERTY_PREFIX = "--color-annotation-"

ROUGH_NOTATION_URL = "https://unpkg.com/rough-notation/lib/rough-notation.iife.js"  # noqa

ROUGH_NOTATION_ANNOTATE = """
  function annotate(el, eff, cat) {
      const c = getComputedStyle(el).getPropertyValue('%(pre)s' + cat);
      const a = RoughNotation.annotate(el, {type: eff, color: c});
      a.show();
  }
""" % {"pre": ANNOTATION_COLOR_PROPERTY_PREFIX}

ANNOTATION_MARKUP = '<span onclick="annotate(this, \'%(eff)s\', \'%(cat)s\')">'


class Writer(HTMLWriter):
    """Writer for generating impress.js output."""

    default_stylesheets = ["minimal.css", "impressjs.css"]

    default_slide_size = "1920x1080"
    default_font_size = "45px"

    settings_spec = frontend.filter_settings_spec(
        HTMLWriter.settings_spec,
        stylesheet_path=(
            'Comma separated list of stylesheet paths. '
            'Relative paths are expanded if a matching file is found in '
            'the --stylesheet-dirs. With --link-stylesheet, '
            'the path is rewritten relative to the output HTML file. '
            '(default: "%s")' % ','.join(default_stylesheets),
            ["--stylesheet-path"],
            {
                "metavar": "<file[,file,...]>",
                "overrides": "stylesheet",
                "validator": frontend.validate_comma_separated_list,
                "default": default_stylesheets,
            }
        ),
    )

    settings_spec = settings_spec + (
        "ImpressJS Writer Options",
        "",
        (
            (
                'Slide size. (default: %s)' % default_slide_size,
                ["--slide-size"],
                {
                    "default": default_slide_size,
                }
            ),
            (
                'Font size. (default: %s)' % default_font_size,
                ["--font-size"],
                {
                    "default": default_font_size,
                }
            ),
        )
    )

    def __init__(self):
        super().__init__()
        self.translator_class = ImpressJSTranslator


class ImpressJSTranslator(HTMLTranslator):
    """Translator for generating impress.js markup."""

    script_impressjs = HTMLTranslator.script_defer % IMPRESS_JS_URL
    script_impressjs_init = HTMLTranslator.script % IMPRESS_JS_INIT

    script_rough_notation = HTMLTranslator.script_defer % ROUGH_NOTATION_URL
    script_annotate = HTMLTranslator.script % ROUGH_NOTATION_ANNOTATE

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.document.settings.slide_size.lower() == "a4":
            self.step_width, self.step_height = 1125, 795
        else:
            width, height = self.document.settings.slide_size.split("x")
            self.step_width, self.step_height = int(width), int(height)

        self.font_size = self.document.settings.font_size

        # add attributes to keep track of the field data
        self.__fields = {}
        self.__field_name, self.__field_body = None, None

        # use a default horizontal step of one step width
        self.__fields["data-rel-x"] = self.step_width

    def starttag(self, node, *args, **kwargs):
        styles = node.attributes.pop("styles", {})
        if len(styles) > 0:
            if "custom" not in node.attributes:
                node.attributes["custom"] = {}
            style = " ".join(f"{k}: {v};" for k, v in styles.items()).strip()
            node.attributes["custom"]["style"] = style
        return super().starttag(node, *args, **kwargs)

    def visit_document(self, node):
        # add attributes for impress.js
        node.attributes["ids"].append("impress")
        node.attributes["custom"] = {
            "data-width": str(self.step_width),
            "data-height": str(self.step_height),
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
        self.head.append(ImpressJSTranslator.script_annotate)

        # add dynamic styles for impress.js
        impress_js_style = IMPRESS_JS_STYLE % {
            "width": self.step_width,
            "height": self.step_height,
            "font_size": self.font_size,
        }
        self.head.append(HTMLTranslator.embedded_stylesheet % impress_js_style)

    def depart_docinfo(self, node):
        # wrap docinfo in a step with a title
        super().depart_docinfo(node)
        self.docinfo.insert(0, '<section class="step" id="docinfo">\n')
        self.docinfo.insert(1, f'<h1>{self.title[0]}</h1>\n')
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
        impressjs_attrs = {}
        attr_names = {k for k in self.__fields if k in IMPRESS_JS_ATTRS}
        for name in attr_names:
            impressjs_attrs[name] = self.__fields.pop(name)
        node.attributes["custom"] = impressjs_attrs
        super().visit_section(node)

    def depart_section(self, node):
        # close the slide body contents div
        self.body.append('</div>\n')
        super().depart_section(node)

    def visit_title(self, node):
        # wrap title h1 in a header
        self.body.append('<header>\n')
        super().visit_title(node)

    def depart_title(self, node):
        self.body.append('</header>\n')
        super().depart_title(node)

        # wrap the slide body contents in a div
        styles = {"perspective": "1000px"}
        layout = self.__fields.pop("layout", None)
        if layout is not None:
            styles["display"] = "grid"
            styles["grid-template-areas"] = f"'{layout}'"
        style = " ".join(f"{k}: {v};" for k, v in styles.items())
        self.body.append(f'<div class="main" style="{style}">\n')

    def visit_container(self, node):
        classes = node.attributes["classes"]
        for class_ in classes:
            prefix = "layout-"
            if class_.startswith(prefix):
                area = class_[len(prefix):]
                node.attributes["styles"] = {"grid-area": area}
                classes.remove(class_)
        super().visit_container(node)

    def visit_reference(self, node):
        # generate clickable '<span>' for annotation
        refuri = node.get("refuri", "")
        annotation = refuri.startswith(ANNOTATION_PREFIX)
        if not annotation:
            super().visit_reference(node)
        else:
            effect, *rest = refuri[len(ANNOTATION_PREFIX):].split("/")
            category = rest[0] if len(rest) == 1 else "default"
            markup = ANNOTATION_MARKUP % {"eff": effect, "cat": category}
            self.body.append(markup)
        node.attributes["_annotation"] = annotation

    def depart_reference(self, node):
        annotation = node.attributes.pop("_annotation", False)
        if not annotation:
            super().depart_reference(node)
        else:
            self.body.append('</span>')
