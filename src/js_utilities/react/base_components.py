"""This module provides TypedDict structures that can be converted to React components.

This module defines the _ReactComponent and ReactComponent classes that represent the base structure and
attributes of a React component, respectively.

Example:

    >>> from js_utilities.react.base_components  import ReactComponent
    >>> child_component = ReactComponent(type="p", children="Hello, world.")
    >>> parent_component = ReactComponent(name='my-component', children=[child_component], type="div")
    >>> print(parent_component)
            {
                'name': 'my-component',
                'is_functional': False,
                'type': 'div',
                'children': [{'type': 'p', 'children': 'Hello, world.' }]
            }
"""
from __future__ import annotations

from typing import TypedDict

from js_utilities.base_types import HTML_ELEMENTS


class _ReactComponent(TypedDict, total=False):
    """A private dictionary that represents the base structure of a React component.

    Attributes:

        name: The name of the React component.
        is_functional: Whether the React component is functional or class-based.
        children: The children of the React component. It can be a list of _ReactComponent objects,
                  a string, a boolean, or an integer.
    """

    name: str
    is_functional: bool
    children: list[ReactComponent] | str | bool | int
    props: dict[str, str | bool | int]


class ReactComponent(_ReactComponent):
    """A dictionary that represents a React component.

    Attributes:

        type: The HTML element type of the React component.
    """

    type: HTML_ELEMENTS
