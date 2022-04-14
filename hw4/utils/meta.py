from typing_extensions import Self
from typing import Any, Callable, Dict


def metaclass_factory(transform: Callable = None, value_transform: Callable = None):
    is_dunder_method = lambda attr: attr.startswith("__") and attr.endswith("__")
    _transform = _value_transform = lambda x: x

    if transform:
        _transform = lambda attr: attr if is_dunder_method(attr) else transform(attr)
    if value_transform:
        _value_transform = lambda attr: transform(attr)

    class Meta:
        def __new__(
            cls, name: str, bases: Any, attrs: Dict[str, Any]
        ) -> Self:
            custom_attrs = {
                _transform(key): _value_transform(value) for key, value in attrs.items()
            }
            return type(name, bases, custom_attrs)

    return Meta


PrefixMeta = metaclass_factory(transform=lambda x: "custom_" + x)
