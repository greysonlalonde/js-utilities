"""A module for representing HTML elements as dictionaries.

This module provides two classes, `_HTMLElement` and `HTMLElement`, that represent HTML elements as dictionaries with
various attributes. The `_HTMLElement` class is a base class that can be used to represent generic HTML elements, while
the `HTMLElement` class adds a `tag` attribute to represent a specific HTML tag name.

Example usage:

    >>> from js_utilities.vanilla.base_components import HTMLElement
    >>> div = HTMLElement(tag="div", content="Hello, world!", attributes={"class": "my-class"})
    >>> div
    {'tag': 'div', 'content': 'Hello, world!', 'attributes': {'class': 'my-class'}}
"""

from __future__ import annotations

from typing import TypedDict


class _HTMLElement(TypedDict, total=False):
    """A dictionary representing an HTML element.

    Attributes:

        attributes: A dictionary of attribute name-value pairs for the HTML element.
        content: The content of the HTML element.
    """

    attributes: dict[str, str | dict]
    content: str


class HTMLElement(_HTMLElement):
    """A dictionary representing an HTML element with a tag name.

    Attributes:
        tag: The tag name for the HTML element.
    """

    tag: str
