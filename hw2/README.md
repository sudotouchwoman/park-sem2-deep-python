# **Homework 2:** HTML parser implementation

Problem: implement function `parse_html` which accepts html string 
and performs parsing by tags with provided callbacks.

The only redesign I performed was splitting actual parsing from callbacks: first, the
string is being parsed using regular expressions (`re` builtin package), yielding `Tag` object with the root of obtained DOM tree.

Then, `describe` method may be called from this object with the actual callbacks.

Unit-tests are written using `pytest` and `mock`.
In order to run them, run: `python3 -m pytest` from this directory in order to avoid problems with imports.
