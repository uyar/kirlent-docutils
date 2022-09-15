# Copyright 2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""reveal.js writer for docutils."""

from pathlib import Path

from docutils import frontend

from .slides import SlidesTranslator
from .slides import Writer as SlidesWriter
from .utils import stylesheet_path_option


REVEALJS_URL = "file://%(path)s" % {
    "path": Path(__file__).parent / "bundled" / "reveal.js",
}

REVEALJS_INIT = """
  window.addEventListener('DOMContentLoaded', () => {
      Reveal.initialize({
          width: '%(width)d',
          height: '%(height)d',
          center: %(center)s,
          transition: '%(transition)s'
      });
  }, false);
"""


class Writer(SlidesWriter):
    """Writer for generating reveal.js output."""

    default_stylesheets = ["kirlent_revealjs.css"]

    default_transition = "none"
    default_center_vertical = False

    settings_spec = frontend.filter_settings_spec(
        SlidesWriter.settings_spec,
        stylesheet_path=stylesheet_path_option(default_stylesheets),
    )

    settings_spec = settings_spec + (
        "RevealJS Writer Options",
        "",
        (
            (
                'Transition effect. (default: %(effect)s)' % {
                    "effect": default_transition
                },
                ["--transition"],
                {
                    "default": default_transition,
                }
            ),
            (
                'Vertically center slides. (default: %(center)s)' % {
                    "center": default_center_vertical,
                },
                ["--center-vertical"],
                {
                    "default": default_center_vertical,
                    "validator": frontend.validate_boolean,
                }
            ),
        )
    )

    def __init__(self):
        super().__init__()
        self.translator_class = RevealJSTranslator


class RevealJSTranslator(SlidesTranslator):
    """Translator for generating reveal.js markup."""

    script_revealjs = SlidesTranslator.script_defer % {"src": REVEALJS_URL}
    script_revealjs_init = SlidesTranslator.script % {"code": REVEALJS_INIT}

    pause_class = "fragment"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.center_vertical = self.document.settings.center_vertical
        self.transition = self.document.settings.transition

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
            "center": "true" if self.center_vertical else "false",
            "transition": self.transition,
        })
