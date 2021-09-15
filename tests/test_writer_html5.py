import re
from functools import partial

from docutils.core import publish_parts

from kirlent.docutils.html5 import Writer


publish_html = partial(publish_parts, writer=Writer())


CHAPTER = "Chapter Title\n=============\n\nchapter text\n\n"
SECTION = "Section Title\n-------------\n\nsection text\n\n"


def test_writer_should_not_generate_xml_declaration():
    html = publish_html("text\n")
    assert "<?xml" not in html["head_prefix"]


def test_writer_should_not_generate_xml_attributes():
    html = publish_html("text\n")
    assert '<html lang="en">' in html["head_prefix"]


def test_writer_should_not_put_space_before_closing_slash_in_meta_content_type():
    html = publish_html("text\n")
    assert '<meta charset="utf-8"/>' in html["meta"]


def test_writer_should_not_put_space_before_closing_slash_in_meta_generator():
    html = publish_html("text\n")
    assert re.search(r'<meta name="generator" content=".*"/>', html["meta"]) is not None


def test_writer_should_not_put_space_before_closing_slash_in_meta():
    html = publish_html(":author: Author\n\ntext\n")
    assert '<meta name="author" content="Author"/>' in html["meta"]


def test_writer_should_not_put_space_before_closing_slash_in_stylesheet_link():
    html = publish_html("text\n", settings_overrides={"embed_stylesheet": False})
    assert re.search(r'<link rel="stylesheet".*[^ ]/>', html["stylesheet"]) is not None


def test_writer_should_not_generate_type_attribute_for_stylesheet_link():
    html = publish_html("text\n", settings_overrides={"embed_stylesheet": False})
    assert "type=" not in html["stylesheet"]


def test_writer_should_not_generate_type_attribute_for_style():
    html = publish_html("text\n")
    assert "type=" not in html["stylesheet"]


def test_writer_should_not_put_space_before_closing_slash_in_void_element():
    html = publish_html("text 1\n\n----\n\ntext 2\n\n")
    assert "<hr/>" in html["body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_list_item():
    html = publish_html("- text\n")
    assert "<li>text</li>" in html["body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_list_item():
    html = publish_html("- par 1\n\n  par 2\n")
    assert "<li><p>par 1</p>\n<p>par 2</p>\n</li>" in html["body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_table_entry():
    html = publish_html("+------+\n| text |\n+------+\n")
    assert "<td>text</td>" in html["body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_table_entry():
    html = publish_html("+-------+\n| par 1 |\n|       |\n| par 2 |\n+-------+\n")
    assert "<td><p>par 1</p>\n<p>par 2</p>\n</td>" in html["body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_definition():
    html = publish_html("term\n  text\n")
    assert "<dd>text</dd>" in html["body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_definition():
    html = publish_html("term\n  par 1\n\n  par 2\n")
    assert "<dd><p>par 1</p>\n<p>par 2</p>\n</dd>" in html["body"]


def test_writer_should_not_generate_paragraph_for_single_paragraph_field_body():
    html = publish_html(SECTION + ":field: text\n")
    assert "<dd>text</dd>" in html["body"]


def test_writer_should_generate_paragraphs_for_multiple_paragraph_field_body():
    html = publish_html(SECTION + ":field: par 1\n\n      par 2\n")
    assert "<dd><p>par 1</p>\n<p>par 2</p>\n</dd>" in html["body"]


def test_writer_should_generate_break_instead_of_line_block_div():
    html = publish_html("| line 1\n| line 2\n")
    assert "line 1<br/>\nline 2<br/>" in html["body"]


def test_writer_should_not_generate_colgroup_under_table():
    html = publish_html("+------+\n| text |\n+------+\n")
    assert "<colgroup>" not in html["body"]


def test_writer_should_not_generate_custom_classes_for_docinfo():
    html = publish_html(":author: Author\n\ntext\n")
    assert '<dl class="docinfo">' in html["html_body"]


def test_writer_should_not_generate_custom_classes_for_list():
    html = publish_html("- text\n")
    assert "<ul>" in html["body"]


def test_writer_should_not_generate_custom_classes_for_table():
    html = publish_html("+------+\n| text |\n+------+\n")
    assert "<table>" in html["body"]


def test_writer_should_not_generate_container_class_for_container():
    html = publish_html(".. container:: name\n\n   text\n")
    assert "container" not in html["body"]


def test_writer_should_generate_container_class_for_container_when_explicit():
    html = publish_html(".. container:: container\n\n   text\n")
    assert '<div class="container">' in html["body"]


def test_writer_should_not_generate_docutils_class_for_container():
    html = publish_html(".. container:: name\n\n   text\n")
    assert "docutils" not in html["body"]


def test_writer_should_not_generate_docutils_class_for_literal():
    html = publish_html("``text``\n")
    assert "docutils" not in html["body"]


def test_writer_should_not_generate_docutils_class_for_transition():
    html = publish_html("text 1\n\n----\n\ntext 2\n\n")
    assert "docutils" not in html["body"]


def test_writer_should_not_generate_custom_classes_for_table_head_entry():
    html = publish_html("+------+\n| head |\n+======+\n| text |\n+------+\n")
    assert "<th>head</th>" in html["body"]


def test_writer_should_not_generate_custom_classes_for_reference():
    html = publish_html("https://tekir.org/\n")
    assert '<a href="https://tekir.org/">https://tekir.org/</a>' in html["body"]
