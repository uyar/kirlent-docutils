import re
from functools import partial

from docutils.core import publish_parts


publish_html = partial(publish_parts, writer_name="kirlent_docutils.impressjs")


PREAMBLE = ".. title:: Document Title\n\n:author: Author\n\n"
SLIDE = "----\n\n%(f)s\n\nSlide Title %(n)d\n=============\n\nContent %(n)d\n\n"


def test_writer_should_generate_script_for_impress_js():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script defer src=".*\bimpress.js"></script>', html["head"]) is not None


def test_writer_should_generate_script_for_initializing_impress_js():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<script>.*\bimpress\(\).init\(\);.*</script>', html["head"], re.DOTALL) is not None


def test_writer_should_generate_main_element_with_id_impress():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<main [^>]*\bid="impress"', html["html_body"]) is not None


def test_writer_should_wrap_docinfo_in_a_step():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section [^>]*\bid="docinfo"[^>]*\bclass="slide step"', html["html_body"]) is not None


def test_writer_should_generate_step_for_section():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section .*\bclass="slide step"', html["html_body"]) is not None


def test_writer_should_set_default_rel_x_on_first_slide():
    html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
    assert re.search(r'<section .*\bdata-rel-x="1920"', html["html_body"]) is not None


# def test_writer_should_generate_perspective_for_slide_contents():
#     html = publish_html(PREAMBLE + (SLIDE % {"n": 1, "f": ""}))
#     assert '<div class="main" style="perspective: 1000px;">' in html["html_body"]
