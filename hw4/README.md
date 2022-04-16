# **Metaclasses and Descriptors**

Metaclasses enable us to modify the process of class creation,
which always ends up with `type` call, as `type` is the global metaclass in Python

In this example, metaclass in used in order to modify names of attributes, which is a little cumbresome,
but a nice tool in general.

Descriptors can suit different tasks, but in this example are used in order to ensure typing
(forbid invalid types for class attributes)


Tests are located in the `test/` directory and can be run via `python -m pytest` command (or `python3`, based on your setup)