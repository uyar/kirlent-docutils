import re
from functools import partial

from docutils.core import publish_parts


publish_html = partial(publish_parts, writer_name="kirlent.docutils.impressjs")


PREAMBLE = ".. title:: Document Title\n\n:author: Author\n\n"
SLIDE = "----\n\n%(f)s\n\nSlide Title %(n)d\n=============\n\nContent %(n)d\n\n"


def test_writer_should_generate_script_for_impress_js():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script defer src=".*\bimpress.js"></script>', html["head"]) is not None


def test_writer_should_generate_script_for_initialiazing_impress_js():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script>.*\bimpress\(\).init\(\);.*</script>', html["head"], re.DOTALL) is not None


def test_writer_should_generate_style_for_impress_js_root_settings():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<style>.*:root {[^}]+}.*</style>', html["head"], re.DOTALL) is not None


def test_writer_should_generate_style_for_impress_js_step_settings():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<style>.*\.step {[^}]+}\s*</style>', html["head"], re.DOTALL) is not None


def test_writer_should_generate_root_with_id_impress():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<main .*\bid="impress"', html["html_body"]) is not None


def test_writer_should_set_default_width_on_root():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<main .*\bdata-width="1280"', html["html_body"]) is not None


def test_writer_should_set_default_height_on_root():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<main .*\bdata-height="720"', html["html_body"]) is not None


def test_writer_should_wrap_docinfo_in_a_step():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section .*\bid="docinfo".*\bclass="step"', html["html_body"]) is not None


def test_writer_should_generate_title_heading_in_docinfo_step():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '<h1>Document Title</h1>' in html["html_body"]


def test_writer_should_not_generate_markup_for_transition():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '<hr' not in html["body"]


def test_writer_should_not_generate_markup_for_field_list():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ":key: val"}))
    assert ('<dl' not in html["body"]) and ('</dl' not in html["body"])


def test_writer_should_not_generate_markup_for_field_name():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ":key: val"}))
    assert ('<dt' not in html["body"]) and ('</dt' not in html["body"])


def test_writer_should_not_generate_markup_for_field_body():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ":key: val"}))
    assert ('<dd' not in html["body"]) and ('</dd' not in html["body"])


def test_writer_should_not_generate_text_for_field_name():
    html = publish_html(PREAMBLE + ":key: val\n")
    assert 'key' not in html["body"]


def test_writer_should_not_generate_text_for_field_body():
    html = publish_html(PREAMBLE + ":key: val\n")
    assert 'val' not in html["body"]


def test_writer_should_generate_step_for_section():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section .*\bclass="step"', html["body"]) is not None


def test_writer_should_set_default_rel_x_on_first_step():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section .*\bdata-rel-x="1280"', html["body"]) is not None


def test_writer_should_generate_wrap_title_in_header():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '<header>\n<h2>Slide Title 1</h2>\n</header>\n' in html["body"]


def test_writer_should_generate_div_main_for_slide_contents():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert '</header>\n<div class="main"' in html["body"]


# def test_writer_should_generate_perspective_for_slide_contents():
#     html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
#     assert '<div class="main" style="perspective: 1000px;">' in html["body"]


def test_writer_should_generate_script_for_rough_notation():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script defer src=".*\brough-notation\b.*.js"></script>', html["head"]) is not None


def test_writer_should_generate_script_for_annotating_elements():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script>\s*function annotate\(.*</script>', html["head"], re.DOTALL) is not None


def test_writer_should_generate_onclick_event_for_reference_with_annotation():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "`Tekir <annotate://box>`_\n")
    assert '<span onclick="annotate(this, \'box\', \'default\')">Tekir</span>' in html["body"]


def test_writer_should_generate_onclick_event_for_reference_with_annotation_category():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "`Tekir <annotate://box/callout>`_\n")
    assert '<span onclick="annotate(this, \'box\', \'callout\')">Tekir</span>' in html["body"]


def test_writer_should_generate_regular_link_for_reference_without_annotation():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}) + "`Tekir <https://tekir.org/>`_\n")
    assert '<a href="https://tekir.org/">Tekir</a>' in html["body"]
