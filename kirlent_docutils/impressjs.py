# Copyright 2020-2022 H. Turgut Uyar <uyar@tekir.org>
#
# kirlent_docutils is released under the BSD license.
# Read the included LICENSE.txt file for details.

"""impress.js writer for docutils."""

from pathlib import Path

from docutils import frontend

from .slides import SlidesTranslator
from .slides import Writer as SlidesWriter


IMPRESSJS_URL = "file://%(path)s" % {
    "path": Path(__file__).parent / "bundled" / "impress.js",
}

IMPRESSJS_INIT = """
  window.addEventListener('DOMContentLoaded', () => {
      impress().init();
  }, false);
"""

IMPRESSJS_STYLE = """
  .step {
    width: %(width)dpx;
    height: %(height)dpx;
  }
"""

IMPRESSJS_ATTRS = {
    "data-x", "data-y", "data-z",
    "data-rel-x", "data-rel-y", "data-rel-z",
    "data-rotate-x", "data-rotate-y", "data-rotate-z",
    "data-rotate", "data-rotate-order",
    "data-scale",
}


class Writer(SlidesWriter):
    """Writer for generating impress.js output."""

    default_stylesheets = SlidesWriter.default_stylesheets + ["impressjs.css"]

    default_transition_duration = 1000
    default_min_scale = 0
    default_max_scale = 3

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
        "ImpressJS Writer Options",
        "",
        (
            (
                'Transition duration in miliseconds. (default: %(td)d)' % {
                    "td": default_transition_duration,
                },
                ["--transition-duration"],
                {
                    "default": default_transition_duration,
                    "validator": frontend.validate_nonnegative_int,
                }
            ),
            (
                'Minimum scale. (default: %(min)d)' % {
                    "min": default_min_scale,
                },
                ["--min-scale"],
                {
                    "default": default_min_scale,
                }
            ),
            (
                'Maximum scale. (default: %(max)d)' % {
                    "max": default_max_scale,
                },
                ["--max-scale"],
                {
                    "default": default_max_scale,
                }
            ),
        )
    )

    def __init__(self):
        super().__init__()
        self.translator_class = ImpressJSTranslator


class ImpressJSTranslator(SlidesTranslator):
    """Translator for generating impress.js markup."""

    script_impressjs = SlidesTranslator.script_defer % {"src": IMPRESSJS_URL}
    script_impressjs_init = SlidesTranslator.script % {"code": IMPRESSJS_INIT}

    pause_class = "substep"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.transition_duration = self.document.settings.transition_duration
        self.min_scale = self.document.settings.min_scale
        self.max_scale = self.document.settings.max_scale

        # use a default horizontal step of one step width
        self._fields["data-rel-x"] = self.slide_width

    def visit_document(self, node):
        # add attributes for impress.js
        node.attributes["ids"].append("impress")
        node.attributes["_custom"] = {
            "data-width": str(self.slide_width),
            "data-height": str(self.slide_height),
            "data-transition-duration": str(self.transition_duration),
            "data-min-scale": str(self.min_scale),
            "data-max-scale": str(self.max_scale),
        }
        super().visit_document(node)

    def depart_document(self, node):
        super().depart_document(node)

        # add code for impress.js
        self.head.append(ImpressJSTranslator.script_impressjs)
        self.head.append(ImpressJSTranslator.script_impressjs_init)

        # add dynamic styles for impress.js
        style = IMPRESSJS_STYLE % {
            "width": self.slide_width,
            "height": self.slide_height,
        }
        self.head.append(SlidesTranslator.embedded_stylesheet % style)

    def depart_docinfo(self, node):
        node.attributes["_docinfo_class"] = "step"
        super().depart_docinfo(node)

    def visit_section(self, node):
        # start a step
        node.attributes["classes"].insert(0, "step")
        step_attrs = {}
        attr_names = {k for k in self._fields if k in IMPRESSJS_ATTRS}
        for name in attr_names:
            step_attrs[name] = self._fields.pop(name)
        node.attributes["_custom"] = step_attrs
        super().visit_section(node)
