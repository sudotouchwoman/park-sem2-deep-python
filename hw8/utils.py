from typing import Dict


class HTMLTag:
    def __init__(self, name: str, content: str, attrs: Dict[str, str]) -> None:
        self.name = name
        self.content = content
        self.attrs = attrs


class HTMLTagSlotted:
    __slots__ = ("name", "content", "attrs", "__weakref__")

    def __init__(self, name: str, content: str, attrs: Dict[str, str]) -> None:
        self.name = name
        self.content = content
        self.attrs = attrs


def tag_factory(name):
    return HTMLTag(name, f"tag-{name}", {"class": "body"})


def slotted_tag_factory(name):
    return HTMLTagSlotted(name, f"tag-{name}", {"style": "bold"})
