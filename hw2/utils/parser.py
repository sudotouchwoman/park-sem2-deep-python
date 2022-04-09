"""
Simple recursive parser for HTML
using regular expressions
"""

from dataclasses import dataclass
from abc import ABC
import re


class HTML(ABC):
    """
    Namespace for constants related to HTML tags regex,
    with simple example document provided
    """

    OPEN_TAG_REGEX = r"^<([!a-zA-z][a-zA-z0-9\-\s=\"\{\}\(\),\.;'_/:@]*)>"
    CLOSED_TAG_REGEX = r"^</([!a-zA-z][a-zA-z0-9\-\s=\"\{\}\(\),\.;'_/:@]*)>"
    DATA_REGEX = r"^([^<]+)"
    EXAMPLE = """
<html>
    <head>
        <title>{% block title %}{% endblock %}</title>
        {%block styles%}
        {%endblock%}
        {%block icon%}
        {%endblock%}
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
    """


@dataclass
class Tag:
    """
    Represents HTML tag, handles its contents
    (inner tags and plain text)
    """

    name: str
    children: list

    def __init__(self, tag_name) -> None:
        self.name = tag_name
        self.children = []

    def subtags(self):
        return filter(lambda x: isinstance(x, Tag), self.children)

    def content(self):
        return filter(lambda x: isinstance(x, str), self.children)

    def describe(self, on_open, on_close, on_content, skip_root=False):
        '''
        Recursively traverses the tag tree.

        Arguments:
            `on_open`, `on_close`: callbacks, is called with tag's name as argument
            `on_content`: callback, is called with the tag's inner plain text as argument
            `skip_root`: `bool`, whether to trigger callbacks on self
        '''
        if not skip_root: on_open(self.name)
        for tag in self.subtags():
            tag.describe(on_open, on_close, on_content)
        content = "".join(self.content())
        if not skip_root: on_content(content)
        if not skip_root: on_close(self.name)


def parse_html(html: str):
    '''
    Parse given html string (in a recursive manner)
    Arguments:
        `html`: `str`, string to parse
    Returns:
        `Tag` object with root of the DOM tree
    Raises:
        `TypeError` if not a string was given
        `RuntimeError` if parsing error is encountered
    '''
    if not isinstance(html, str): raise TypeError(f'Expected HTML string object')

    open_tag_regex, closed_tag_regex, content_regex = map(
        re.compile,
        (HTML.OPEN_TAG_REGEX, HTML.CLOSED_TAG_REGEX, HTML.DATA_REGEX),
    )

    # helper function to fetch pattern
    # from the current html string
    # and cut the matched slice from it
    def pull(pattern: re.Pattern, handler) -> bool:
        nonlocal html
        match = pattern.match(html)
        if not match: return False
        html = html[match.end() :]
        handler(match.group())
        return True

    def parse_content(node: Tag):
        nonlocal html
        found_close_tag = False

        def open_tag_handler(tag):
            new_tag = Tag(tag)
            node.children.append(new_tag)
            parse_content(new_tag)

        def closed_tag_handler(_):
            nonlocal found_close_tag
            found_close_tag = True

        def content_handler(content):
            node.children.append(content)

        while not found_close_tag and html:
            if not (
                pull(open_tag_regex, open_tag_handler)
                or pull(closed_tag_regex, closed_tag_handler)
                or pull(content_regex, content_handler)
            ):
                raise RuntimeError(f"Parsing Error: {html}")

    root = Tag('root')
    parse_content(root)
    return root
