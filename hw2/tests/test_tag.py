"""
Unit-tests for Tag class: object creation, representation
Also check adding children to Tag
"""
import pytest
from utils.parser import Tag


@pytest.fixture
def make_tag_name():
    return ("<div>", "<head>", "p", "body")


@pytest.fixture
def make_tag_text():
    return ("Lorem ipsum dolor sit", "Vivamus integer non suscipit taciti mus")


def test_constructor(*make_tag_name):
    tags = map(Tag, make_tag_name)
    for tag, expected_name in zip(tags, make_tag_name):
        assert tag.name == expected_name
        assert str(tag) == f"Tag(name='{expected_name}', __children=[])"


def test_tag_children(make_tag_text):
    body, div = Tag("body"), Tag("div")
    body_text, div_text = make_tag_text

    assert len(tuple(body.subtags())) == 0
    assert len(tuple(div.subtags())) == 0

    body.add_item(div)
    body.add_item(body_text)

    assert len(tuple(body.subtags())) == 1
    assert len(tuple(div.subtags())) == 0

    div.add_item(div_text)

    assert len(tuple(body.content())) == 1
    assert len(tuple(div.content())) == 1

    for text in body.content():
        assert body_text == text

    for text in div.content():
        assert div_text == text


def test_add_item(make_tag_text):
    div = Tag("div")
    text, *_ = make_tag_text

    div.add_item(text)
    div.add_item(Tag("p"))

    with pytest.raises(TypeError) as exc_info:
        div.add_item(42)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, TypeError)
