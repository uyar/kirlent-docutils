# Copyright 2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""reveal.js writer for docutils."""

from pathlib import Path

from docutils import frontend

from .slides import SlidesTranslator
from .slides import Writer as SlidesWriter


REVEAL_JS_PATH = Path(__file__).parent.joinpath("bundled", "reveal.js")

REVEAL_JS_INIT = """
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

    default_stylesheets = ["minimal.css", "revealjs.css"]

    default_transition = "none"
    default_center_vertical = False

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

    settings_spec = settings_spec + (
        "RevealJS Writer Options",
        "",
        (
            (
                'Slide transition effect. (default: %s)' % default_transition,
                ["--transition"],
                {
                    "default": default_transition,
                }
            ),
            (
                'Vertically center slides. (default: %s)' % (
                    default_center_vertical,
                ),
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

    script_revealjs = SlidesTranslator.script_defer % REVEAL_JS_PATH
    script_revealjs_init = SlidesTranslator.script % REVEAL_JS_INIT

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
