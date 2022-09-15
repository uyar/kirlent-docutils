# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Generic HTML5 slides writer for docutils."""

from pathlib import Path
from xml.etree import ElementTree

from docutils import frontend
from docutils.nodes import container

from .html5 import HTMLTranslator
from .html5 import Writer as HTMLWriter
from .utils import stylesheet_path_option


ANNOTATION_PREFIX = "annotate://"

ANNOTATION_COLOR_PROPERTY_PREFIX = "--color-annotation-"

ROUGH_NOTATION_URL = "file://%(path)s" % {
    "path": Path(__file__).parent / "bundled" / "rough-notation.iife.js",
}

ROUGH_NOTATION_ANNOTATE = """
  function annotate(el, eff, cat) {
      const c = getComputedStyle(el).getPropertyValue('%(pre)s' + cat);
      const a = RoughNotation.annotate(el, {type: eff, color: c});
      a.show();
  }
""" % {"pre": ANNOTATION_COLOR_PROPERTY_PREFIX}

ANNOTATION_MARKUP = '<span onclick="annotate(this, \'%(eff)s\', \'%(cat)s\')">'


SLIDE_SIZES = {
    "a4": (1125, 795),
}


class Writer(HTMLWriter):
    """Writer for generating HTML5 slides output."""

    default_stylesheets = ["kirlent_slides.css"]

    default_slide_width = 1920
    default_slide_height = 1080

    settings_spec = frontend.filter_settings_spec(
        HTMLWriter.settings_spec,
        stylesheet_path=stylesheet_path_option(default_stylesheets),
    )

    settings_spec = settings_spec + (
        "HTML5 slides writer Options",
        "",
        (
            (
                'Slide size in pixels. (default: %(width)dx%(height)d)' % {
                    "width": default_slide_width,
                    "height": default_slide_height,
                },
                ["--slide-size"],
                {
                    "default": "%(width)dx%(height)d" % {
                        "width": default_slide_width,
                        "height": default_slide_height,
                    },
                }
            ),
        )
    )

    def __init__(self):
        super().__init__()
        self.translator_class = SlidesTranslator


class SlidesTranslator(HTMLTranslator):
    """Translator for generating HTML5 slides markup."""

    pause_class = ""

    data_attrs = set()

    script_rough_notation = HTMLTranslator.script_defer % {
        "src": ROUGH_NOTATION_URL,
    }
    script_annotate = HTMLTranslator.script % {"code": ROUGH_NOTATION_ANNOTATE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        slide_size_key = self.document.settings.slide_size.lower()
        slide_size = SLIDE_SIZES.get(slide_size_key)
        if slide_size is None:
            slide_size = map(int, slide_size_key.split("x"))
        self.slide_width, self.slide_height = slide_size

        # add attributes to keep track of the field data
        self._fields = {}
        self._field_name, self._field_body = None, None

    def starttag(self, node, *args, **kwargs):
        pause = self._fields.pop("pause", None)
        if pause is not None:
            node.attributes["classes"].append(self.__class__.pause_class)
        return super().starttag(node, *args, **kwargs)

    def visit_document(self, node):
        super().visit_document(node)

        # note the title in order to add it to docinfo later
        self.title.append(node.get("title", ""))

    def depart_document(self, node):
        super().depart_document(node)

        # add code for loading rough notation
        self.head.append(SlidesTranslator.script_rough_notation)
        self.head.append(SlidesTranslator.script_annotate)

    def depart_docinfo(self, node):
        # wrap docinfo in a slide with a title
        super().depart_docinfo(node)
        self.docinfo.insert(0, '<section id="docinfo" class="slide">\n')
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
        value = self._field_body if self._field_body is not None else ""
        self._fields[self._field_name] = value
        self._field_name, self._field_body = None, None

    def visit_Text(self, node):
        # suppress text generation under field names and bodies
        parent = node.parent
        if parent.tagname == "field_name":
            self._field_name = node.astext()
        elif parent.parent.tagname == "field_body":
            self._field_body = node.astext()
        else:
            super().visit_Text(node)

    def visit_section(self, node):
        node.attributes["classes"].insert(0, "slide")
        attrs = {}
        for attr in self.__class__.data_attrs.intersection(self._fields):
            attrs[attr] = self._fields.pop(attr)
        node.attributes["_custom"] = attrs
        super().visit_section(node)

    def depart_section(self, node):
        self.body.append('</div>\n')  # close the slide contents div
        super().depart_section(node)

    def visit_title(self, node):
        self.body.append('<header>\n')  # wrap title in a header
        super().visit_title(node)

    def depart_title(self, node):
        super().depart_title(node)
        self.body.append('</header>\n')

        # wrap the slide contents in a div
        styles = {}
        layout = self._fields.pop("layout", None)
        if layout is not None:
            areas = " ".join(f"'{row}'" for row in layout.splitlines())
            styles["grid-template-areas"] = areas
        slide_contents = container()
        slide_contents.attributes["classes"] = ["content"]
        slide_contents.attributes["_styles"] = styles
        self.visit_container(slide_contents)

    def visit_container(self, node):
        prefix = "layout-"
        classes = node.attributes["classes"]
        for class_ in classes:
            if class_.startswith(prefix):
                area = class_[len(prefix):]
                node.attributes["_styles"] = {"grid-area": area}
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

    def visit_image(self, node):
        # scale SVG images generated from mermaid.js diagrams
        # mermaid.js sets width to 100% and height to diagram height
        if "height" not in node.attributes:
            uri = node.attributes["uri"]
            source = Path(self.document.settings._source).parent / uri
            if source.suffix == ".svg":
                root = ElementTree.parse(source).getroot()
                if root.attrib["id"].startswith("mermaid-"):
                    height = float(root.attrib["height"])
                    scale = 3
                    node.attributes["height"] = str(round(height * scale))
        super().visit_image(node)
