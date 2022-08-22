from functools import partial

from docutils.core import publish_parts


publish_html = partial(publish_parts, writer_name="kirlent_docutils.html5")


def test_writer_should_not_generate_xml_declaration():
    html = publish_html("text\n")
    assert '<?xml' not in html["whole"]


def test_writer_should_not_generate_xml_attributes():
    html = publish_html("text\n")
    assert ' xml' not in html["whole"]


def test_writer_should_not_generate_type_attribute_for_stylesheet_link():
    html = publish_html("text\n", settings_overrides={"embed_stylesheet": False})
    assert 'type=' not in html["whole"]


def test_writer_should_not_generate_type_attribute_for_style():
    html = publish_html("text\n")
    assert 'type=' not in html["whole"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_list_item():
    html = publish_html("- item\n")
    assert '<li>item</li>' in html["html_body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_list_item():
    html = publish_html("- par 1\n\n  par 2\n")
    assert '<li><p>par 1</p>\n<p>par 2</p>\n</li>' in html["html_body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_table_entry():
    html = publish_html("+-------+\n| entry |\n+-------+\n")
    assert '<td>entry</td>' in html["html_body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_table_entry():
    html = publish_html("+-------+\n| par 1 |\n|       |\n| par 2 |\n+-------+\n")
    assert '<td><p>par 1</p>\n<p>par 2</p>\n</td>' in html["html_body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_definition():
    html = publish_html("term\n  def\n")
    assert '<dd>def</dd>' in html["html_body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_definition():
    html = publish_html("term\n  par 1\n\n  par 2\n")
    assert '<dd><p>par 1</p>\n<p>par 2</p>\n</dd>' in html["html_body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_field_body():
    html = publish_html("text\n\n:field: val\n")
    assert '<dd>val</dd>' in html["html_body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_field_body():
    html = publish_html("text\n\n:field: par 1\n\n      par 2\n")
    assert '<dd><p>par 1</p>\n<p>par 2</p>\n</dd>' in html["html_body"]


def test_writer_should_generate_line_break_instead_of_line_block_div():
    html = publish_html("| line 1\n| line 2\n")
    assert 'line 1<br/>\nline 2<br/>' in html["html_body"]


def test_writer_should_not_generate_simple_class_for_docinfo():
    html = publish_html(":author: Author\n\ntext\n")
    assert '<dl class="docinfo">' in html["html_body"]


def test_writer_should_not_generate_simple_class_for_list():
    html = publish_html("- item\n")
    assert '<ul>' in html["html_body"]


def test_writer_should_generate_simple_class_for_list_when_explicit():
    html = publish_html(".. class:: simple\n\n- item\n")
    assert '<ul class="simple">' in html["html_body"]


def test_writer_should_not_generate_container_class_for_container():
    html = publish_html(".. container:: name\n\n   text\n")
    assert 'container' not in html["html_body"]


def test_writer_should_generate_container_class_for_container_when_explicit():
    html = publish_html(".. container:: container\n\n   text\n")
    assert '<div class="container">' in html["html_body"]


def test_writer_should_not_generate_docutils_class_for_container():
    html = publish_html(".. container:: name\n\n   text\n")
    assert 'docutils' not in html["html_body"]


def test_writer_should_generate_docutils_class_for_container_when_explicit():
    html = publish_html(".. container:: docutils\n\n   text\n")
    assert '<div class="docutils">' in html["html_body"]


def test_writer_should_not_generate_docutils_class_for_literal():
    html = publish_html("``text``\n")
    assert 'docutils' not in html["html_body"]


def test_writer_should_not_generate_docutils_class_for_transition():
    html = publish_html("text 1\n\n----\n\ntext 2\n\n")
    assert 'docutils' not in html["html_body"]


def test_writer_should_not_generate_title_class_for_h1():
    html = publish_html("Title\n=====\n\ntext\n")
    assert '<h1>Title</h1>' in html["html_body"]


def test_writer_should_not_generate_head_class_for_table_head_entry():
    html = publish_html("+------+\n| head |\n+======+\n| text |\n+------+\n")
    assert '<th>head</th>' in html["html_body"]


def test_writer_should_not_generate_internal_reference_classes_for_internal_reference():
    html = publish_html("text\n\nsection\n-------\n\n`section`_\n")
    assert '<a href="#section">section</a>' in html["html_body"]


def test_writer_should_not_generate_target_class_for_internal_reference():
    html = publish_html("_`text`")
    assert '<span id="text">' in html["html_body"]


def test_writer_should_not_generate_external_reference_classes_for_external_reference():
    html = publish_html("https://tekir.org/\n")
    assert '<a href="https://tekir.org/">https://tekir.org/</a>' in html["html_body"]


def test_writer_should_not_generate_literal_block_class_for_pre():
    html = publish_html("::\n\n  text")
    assert '<pre>' in html["html_body"]


def test_writer_should_generate_literal_class_for_pre_when_explicit():
    html = publish_html(".. class:: literal-block\n\n::\n\n  text")
    assert '<pre class="literal-block">' in html["html_body"]
