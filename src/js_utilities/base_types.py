"""A module for defining a Literal type of HTML element tag names.

This module provides a single `Literal` type called `HTML_ELEMENTS`,
which represents a list of valid HTML element tag names. The `Literal`
type is used to ensure that only valid tag names are used as arguments in
functions that expect an HTML element tag name.

Example usage:
    >>> from __future__ import annotations
    >>> from typing import Union
    >>> from js_utilities.base_types import HTML_ELEMENTS
    >>> def create_element(tag: HTML_ELEMENTS | str, content: str) -> dict[str, str]:
    ...     return {'tag': tag, 'content': content}
    ...
    >>> create_element('div', 'Hello, world!')
    {'tag': 'div', 'content': 'Hello, world!'}
"""

from typing import Literal

HTML_ELEMENTS = Literal[
    'a',
    'abbr',
    'address',
    'area',
    'article',
    'aside',
    'audio',
    'b',
    'bdi',
    'bdo',
    'blockquote',
    'body',
    'br',
    'button',
    'canvas',
    'caption',
    'cite',
    'code',
    'col',
    'colgroup',
    'command',
    'datalist',
    'dd',
    'del',
    'details',
    'dfn',
    'div',
    'dl',
    'dt',
    'em',
    'embed',
    'fieldset',
    'figcaption',
    'figure',
    'footer',
    'form',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'header',
    'hr',
    'html',
    'i',
    'iframe',
    'img',
    'input',
    'ins',
    'kbd',
    'keygen',
    'label',
    'legend',
    'li',
    'main',
    'map',
    'mark',
    'menu',
    'meter',
    'nav',
    'object',
    'ol',
    'optgroup',
    'option',
    'output',
    'p',
    'param',
    'pre',
    'progress',
    'q',
    'rp',
    'rt',
    'ruby',
    's',
    'samp',
    'section',
    'select',
    'small',
    'source',
    'span',
    'strong',
    'sub',
    'summary',
    'sup',
    'table',
    'tbody',
    'td',
    'textarea',
    'tfoot',
    'th',
    'thead',
    'time',
    'tr',
    'track',
    'u',
    'ul',
    'var',
    'video',
    'wbr',
]
