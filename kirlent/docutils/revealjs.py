# Copyright 2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""reveal.js writer for docutils."""

from docutils import frontend

from .slides import SlidesTranslator
from .slides import Writer as SlidesWriter


REVEAL_JS_URL = "https://cdn.jsdelivr.net/npm/reveal.js@3.7.0/js/reveal.min.js"

REVEAL_JS_INIT = """
  window.addEventListener('DOMContentLoaded', () => {
      Reveal.initialize({
          width: '%(width)d',
          height: '%(height)d'
      });
  }, false);
"""


class Writer(SlidesWriter):
    """Writer for generating impress.js output."""

    default_stylesheets = ["minimal.css", "revealjs.css"]

    settings_spec = frontend.filter_settings_spec(
        SlidesWriter.settings_spec,
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

    def __init__(self):
        super().__init__()
        self.translator_class = RevealJSTranslator


class RevealJSTranslator(SlidesTranslator):
    """Translator for generating reveal.js markup."""

    script_revealjs = SlidesTranslator.script_defer % REVEAL_JS_URL
    script_revealjs_init = SlidesTranslator.script % REVEAL_JS_INIT

    def visit_document(self, node):
        # add attributes for reveal.js
        node.attributes["classes"].append("reveal")
        super().visit_document(node)

    def depart_document(self, node):
        self.body_pre_docinfo.append('<div class="slides">\n')
        self.body.append('</div>\n')
        super().depart_document(node)

        # add code for reveal.js
        self.head.append(RevealJSTranslator.script_revealjs)
        self.head.append(RevealJSTranslator.script_revealjs_init % {
            "width": self.slide_width,
            "height": self.slide_height,
        })

    def depart_docinfo(self, node):
        # wrap docinfo in a slide with a title
        super().depart_docinfo(node)
        self.docinfo.insert(0, '<section id="docinfo">\n')
        self.docinfo.insert(1, f'<h1>{self.title[0]}</h1>\n')
        self.docinfo.append('</section>\n')

    def visit_container(self, node):
        classes = node.attributes["classes"]
        if "substep" in classes:
            classes.remove("substep")
            classes.append("fragment")
        super().visit_container(node)
