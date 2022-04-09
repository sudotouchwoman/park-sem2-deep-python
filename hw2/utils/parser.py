from dataclasses import dataclass
from abc import ABC
import re


class HTML(ABC):
    OPEN_TAG_REGEX = r"^<([!a-zA-z][a-zA-z0-9\-\s=\"\{\}\(\),\.;'_/:@]*)>"
    CLOSED_TAG_REGEX = r"^</([!a-zA-z][a-zA-z0-9\-\s=\"\{\}\(\),\.;'_/:@]*)>"
    DATA_REGEX = r"^([^<]+)"
    EXAMPLE = """
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta content="width=device-width, initial-scale=1"> 
        <title>{% block title %}{% endblock %}</title>
        {%block styles%}
        <link href="{{ url_for('static', filename='css/menu.css') }}" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        {%endblock%}
        {%block icon%}
        <link rel="shortcut icon" type="image/png" href="{{ url_for('static', filename='img/404.png') }}">
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

    name: str
    children: list

    def __init__(self, tag_name, root=False) -> None:
        self.name = tag_name
        self.children = []
        self.root = root

    def describe(self, on_open, on_close, on_content):
        if not self.root: on_open(self.name)
        content = ''.join(filter(lambda x: isinstance(x, str), self.children))
        for tag in filter(lambda x: isinstance(x, Tag), self.children):
            tag.describe(on_open, on_close, on_content)
        if not self.root: on_content(content)
        if not self.root: on_close(self.name)


def parse_html(html: str, on_open_tag, on_closed_tag, on_content):
    open_tag_regex, closed_tag_regex, content_regex = map(
        re.compile,
        (HTML.OPEN_TAG_REGEX, HTML.CLOSED_TAG_REGEX, HTML.DATA_REGEX),
    )

    def pull(regex: re.Pattern, handler) -> bool:
        nonlocal html
        match = regex.match(html)
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

    root = Tag('root', root=True)
    parse_content(root)
    root.describe(on_open_tag, on_closed_tag, on_content)


if __name__ == "__main__":
    html = HTML.EXAMPLE

    on_open = lambda t: print(f"Opened tag: {t}")
    on_close = lambda t: print(f"Closed tag: {t}")
    on_content = lambda c: print(f"Found content: {c}") if c.strip() else None

    parse_html(html, on_open, on_close, on_content)
