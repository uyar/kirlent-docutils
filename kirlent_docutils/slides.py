# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""Generic HTML5 slides writer for docutils."""

from pathlib import Path
from xml.etree import ElementTree

from docutils import frontend, nodes

from .html5 import HTMLTranslator
from .html5 import Writer as HTMLWriter
from .utils import stylesheet_path_option


ROUGH_NOTATION_URL = "file://%(path)s" % {
    "path": Path(__file__).parent / "bundled" / "rough-notation.iife.js",
}

ROUGH_NOTATION_SCRIPT = """
  window.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('.annotation').forEach((el) =>
          el.addEventListener('click', (event) => {
              const a = RoughNotation.annotate(el, {type: "underline"});
              a.show();
          }, false));
  }, false);
"""


class Writer(HTMLWriter):
    """Writer for generating HTML5 slides output."""

    default_stylesheets = [
        s.replace("kirlent_html5", "kirlent_slides")
        for s in HTMLWriter.default_stylesheets
    ]

    settings_spec = frontend.filter_settings_spec(
        HTMLWriter.settings_spec,
        stylesheet_path=stylesheet_path_option(default_stylesheets),
    )

    def __init__(self):
        super().__init__()
        self.translator_class = SlidesTranslator


class SlidesTranslator(HTMLTranslator):
    """Translator for generating HTML5 slides markup."""

    pause_class = ""

    annotation_types = {
        "_": "underline",
    }

    data_attrs = set()

    script_rough_notation = HTMLTranslator.script_defer % {
        "src": ROUGH_NOTATION_URL,
    }
    script_annotate = HTMLTranslator.script % {"code": ROUGH_NOTATION_SCRIPT}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        slide_contents = nodes.container()
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

    def visit_emphasis(self, node):
        assert len(node.children) == 1
        assert isinstance(node.children[0], nodes.Text)
        text = node.children[0].astext()
        if (len(text) > 4) and (text[0] == ">") and (text[-1] == "<") \
                and (text[1] == text[-2]):
            annotation_type = SlidesTranslator.annotation_types.get(text[1])
            if annotation_type is not None:
                tag = f'<span class="annotation annotation-{annotation_type}">'
                self.body.append(tag)
                child = nodes.Text(text[2:-2])
                child.parent = node
                node.children = [child]
                node.attributes["_annotation"] = True
        else:
            super().visit_emphasis(node)

    def depart_emphasis(self, node):
        annotation = node.attributes.pop("_annotation", False)
        if annotation:
            self.body.append('</span>')
        else:
            super().depart_emphasis(node)

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
