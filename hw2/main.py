"""
Demo of HTML parsing
The example is loaded from utils
"""
from utils.parser import parse_html, HTML


def main():
    print("HTML Parsing example. This is the original string:")
    print(HTML.EXAMPLE)

    on_open = lambda t: print(f"Opening tag: {t}")
    on_close = lambda t: print(f"Closing tag: {t}")
    on_content = lambda c: print(f"Found content: {c}") if c.strip() else None

    root = parse_html(HTML.EXAMPLE)
    print("This is the parsing result:")
    root.describe(on_open, on_close, on_content, skip_root=True)


if __name__ == "__main__":
    main()
