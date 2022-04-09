"""
Unit-tests for HTML parser implementation
"""
import pytest

from utils.parser import parse_html, Tag


@pytest.fixture()
def make_simple_html_string():
    return """<div>{div_text}<p>{p_text}</p></div><b>{bold_text}</b>"""


@pytest.fixture()
def make_simple_text():
    return {"div_text": "some div text", "p_text": "para text", "bold_text": "bold boi"}


@pytest.fixture()
def load_sample_html():
    with open("data/test_index.html") as file:
        html = file.read()
    return html


def test_parser(mocker, make_simple_html_string, make_simple_text):
    formatted_html = make_simple_html_string.format(**make_simple_text)
    root = parse_html(formatted_html)

    assert isinstance(root, Tag)

    on_begin_stub = mocker.stub(name="begin_stub")
    on_end_stub = mocker.stub(name="end_stub")
    on_content_stub = mocker.stub(name="content_stub")

    root.describe(on_begin_stub, on_end_stub, on_content_stub, skip_root=True)

    assert on_begin_stub.call_count == 3
    assert on_end_stub.call_count == 3
    assert on_content_stub.call_count == 3


def test_parser_on_sample_html(mocker, load_sample_html):
    root = parse_html(load_sample_html)

    assert isinstance(root, Tag)

    on_begin_stub = mocker.stub(name="begin_stub")
    on_end_stub = mocker.stub(name="end_stub")
    on_content_stub = mocker.stub(name="content_stub")

    root.describe(on_begin_stub, on_end_stub, on_content_stub, skip_root=False)

    assert on_begin_stub.call_count > 1
    assert on_end_stub.call_count > 1
    assert on_content_stub.call_count > 1
