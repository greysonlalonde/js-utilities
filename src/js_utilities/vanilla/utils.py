"""js_utilities module.

This module provides a collection of utilities for rendering javascript objects, including
functions for converting between camelCase and snake_case naming conventions for strings or collections of strings.

The camelize + decamelize utilities are inspired/copied from https://github.com/nficano/humps/blob/master/humps/main.py.

Example usage:

    >>> from js_utilities.vanilla.utils import camelize, decamelize
    >>> camelize("hello_world")
    'helloWorld'
    >>> decamelize("helloWorld")
    'hello_world'

Todo:
    Implement functional_component & class_component functions, render method for ReactComponent in generic function.
"""
from __future__ import annotations

import json
import re
from functools import singledispatch
from typing import (
    Any,
    AnyStr,
    Callable,
    Iterable,
    Mapping,
    NoReturn,
    Optional,
    Pattern,
)

from js_utilities.react.base_components import ReactComponent


def add_curls(val: str) -> str:
    """Returns a string surrounded those sweet, sweet curly brackets.

    Typical usage is for adding attributes within javascript elements,
    ex: <Component val={"my_value"}/>.

    Args:
        val: A string value.

    Returns:
        A string surrounded by curly braces.

    Example:
        >>> add_curls("foo")
        "{foo}"
    """
    return f'{{{val}}}'


def add_state(val: Optional[str] = '') -> str:
    """Returns a string representing the state variable in a component.

    Used alone, this is normally for adding the state value to
    data attributes within a functional component.

    Args:
        val: A string value representing a property of the state. Defaults to "".

    Returns:
        A string representing the state variable in a component.

    Example:
        >>> add_state("count")
        "state.count"
    """
    return f"state{f'.{val}' if val else val}"


def add_props(val: Optional[str] = '') -> str:
    """Returns a string representing the props variable in a javascript component.

    Used alone, this is normally for adding the props value to
    data attributes within a functional javascript component.

    Args:
        val: A string value representing a property of the props. Defaults to "".

    Returns:
        A string representing the props variable in a component.

    Example:
        >>> add_props("name")
        "props.name"
    """
    return f"props{f'.{val}' if val else val}"


def add_this(val: Optional[str] = '') -> str:
    """Returns a string representing the `this` keyword in a javascript class component.

    Used alone, this is normally for adding the `this` value to
    data attributes/methods within a javascript class component.

    Args:
        val: A string value representing a property of the class. Defaults to "".

    Returns:
        A string representing the `this` keyword in a class component.

    Example:
        >>> add_this("state")
        "this.state"
    """
    return f'this.{val}'


def add_class_props(val: str) -> str:
    """Returns a string representing the props variable in a class component.


    Used alone, this is normally for adding the `this.props` value to
    data attributes/methods within a javascript class component.

    Args:
        val: A string value representing a property of the props.

    Returns:
        A string representing the props variable in a class component.

    Example:
        >>> add_class_props("name")
        "this.props.name"
    """
    return add_this(add_props(val))


def add_class_state(val: Optional[str] = '') -> str:
    """Returns a string representing the state variable in a javascript class component.

    Used alone, this is normally for adding the `this.state` value to
    data attributes/methods within a class component.

    Args:
        val: A string value representing a property of the state. Defaults to "".

    Returns:
        A string representing the state variable in a class component.

    Example:
        >>> add_class_state("count")
        "this.state.count"
    """
    return add_this(add_state(val))


def const(const_name: str, value: str) -> str:
    """Returns a string representing a constant variable declaration.

    Args:
        const_name: A string value representing the constant variable name.
        value: A string value representing the constant variable value.

    Returns:
        A string representing a constant variable declaration.

    Example:
        >>> const("MAX_VALUE", "10")
        "const MAX_VALUE = 10"
    """
    return f'const {const_name} = {value}'


def ternary_expression(
    condition: str,
    truthy: int | str | bool | type(None),
    falsy: int | str | bool | type(None),
) -> str:
    """Returns the JavaScript ternary expression for the given condition and values.

    Args:
        condition: A string representing the condition to be evaluated.
        truthy: The value to return if the condition is true. It can be an integer, string, boolean or None.
        falsy: The value to return if the condition is false. It can be an integer, string, boolean or None.

    Examples:
        >>> ternary_expression("x > 10", 5, 10)
        '{x > 10 ? 5 : 10}'
        >>> ternary_expression("x > 0", "positive", "negative")
        '{x > 0 ? "positive" : "negative"}'
        >>> ternary_expression("x is not None", True, False)
        '{x is not None ? true : false}'

    Returns:
        A string representing the JavaScript ternary expression for the given condition and values.
    """

    @singledispatch
    def ternary_value(t_value: Any) -> NoReturn:
        """Generic function for rendering truthy and falsy values.

        See Also:
            https://peps.python.org/pep-0443/

        Args:
            t_value: Any string, integer, boolean, null value or Composite type component.

        Returns:
            Composite type component.
        """
        raise ValueError(f'Type of {type(t_value)} is not allowed.')

    @ternary_value.register(ReactComponent)
    def _(_: ReactComponent) -> str:
        raise NotImplementedError

    @ternary_value.register(int)
    @ternary_value.register(str)
    @ternary_value.register(bool)
    def _(t_value: int | str | bool | type(None)) -> str:
        return json.dumps(t_value)

    truthy = ternary_value(truthy)
    falsy = ternary_value(falsy)
    return add_curls(f'{condition} ? {truthy} : {falsy}')


def inline_variable(name: str, props: Optional[Any] = None) -> str:
    """Returns an inline variable string representation.

    Args:
        name: The name of the variable.
        props: The variable's properties. Defaults to None.

    Examples:
        >>> inline_variable("myVar")
        '() => myVar'
        >>> inline_variable("myVar", "props")
        '{props} => myVar'

    Returns:
        A string representation of the inline variable.
    """
    props = add_curls(props) if props else '()'
    return f'{props} => {name}'


def inline_function(
    name: str, props: Optional[Any] = None, value: Optional[Any] = ''
) -> str:
    """Generate a javascript inline function.

    Args:
        name: The name of the function to generate.
        props: A dictionary of function arguments. Defaults to None.
        value: The function body. Defaults to "".

    Examples:
        >>> inline_function('add', {'x': 1, 'y': 2}, 'x + y')
        "(x=1, y=2) => add(x + y)"

    Returns:
        A string representation of the generated inline function.
    """
    props = add_curls(props) if props else ''
    return f'({props}) => {name}({value})'


def arrow_function(
    name: str, props: Optional[Any] = None, value: Optional[Any] = ''
) -> str:
    """Returns an arrow function declaration as a string.

    Args:
        name: The name of the arrow function.
        props: The props of the arrow function. Defaults to None.
        value: The value of the arrow function. Defaults to "".

    Examples:
        >>> arrow_function("addition", ["a", "b"], "return a + b;")
        'addition = (a, b) => {return a + b;}'

    Returns:
        The arrow function declaration as a string.
    """
    return f'{name} = {{ {inline_function(name, props, value)} }}'


def const_arrow_function(
    name: str, props: Optional[Any] = None, value: Optional[Any] = ''
) -> str:
    """Returns a JavaScript constant with an arrow function expression.

    Args:
        name: The name of the constant.
        props: The function arguments, as a string or a list of strings. If None, no argument is declared.
        value: The function body, as a string or an expression. If "", an empty arrow function is returned.

    Examples:
        >>> const_arrow_function("add", ["x", "y"], "x + y")
        "const add = (x, y) => x + y;"
        >>> const_arrow_function("hello", value='"Hello, world!"')
        "const hello = () => "Hello, world!";"

    Returns:
        A string representing the JavaScript constant.
    """
    return const(name, inline_function(name, props, value))


def _class_constructor(state: str) -> str:
    """Returns a string representation of the constructor of a React class component.

    Args:
        state: A string representation of the state of the component.

    Returns:
        A string representation of the constructor of the component.

    Examples:
        >>> component_state = '{ count: 0 }'
        >>> _class_constructor(component_state)
        "constructor(props) { super(props); this.state = { count: 0 }; }"
    """
    class_state = add_class_state()
    internal = f'super(props);{class_state} = {state}'
    return f'constructor(props){add_curls(internal)}'


def return_(components: Optional[str]) -> str:
    """Returns a string representation of the return statement containing the given components.

    Args:
        components: A string representation of the components to be returned.

    Returns:
        A string representation of the return statement.

    Examples:
        >>> return_("componentA")
        'return (componentA)'

        >>> return_("componentA, componentB")
        'return (componentA, componentB)'

        >>> return_(None)
        'return ()'
    """
    return f'return ({components})'


def functional_component(_: ReactComponent) -> NoReturn:
    """

    Args:
        _:
    """
    raise NotImplementedError


def class_component(_: ReactComponent) -> NoReturn:
    """

    Args:
        _:
    """
    raise NotImplementedError


ACRONYM_RE: Pattern[AnyStr] = re.compile(r'([A-Z]+)$|([A-Z]+)(?=[A-Z\d])')
PASCAL_RE: Pattern[AnyStr] = re.compile(r'([^\-_\s]+)')
SPLIT_RE: Pattern[AnyStr] = re.compile(
    r'([\-_\s]*[A-Z]+?[^A-Z\-_\s]*[\-_\s]*)'
)
UNDERSCORE_RE: Pattern[AnyStr] = re.compile(r'(?<=[^\-_\s])[\-_\s]+[^\-_\s]')


def camelize(str_or_iter: list | dict | str) -> list | dict | str:
    """Convert a string or collection of strings from snake_case to camelCase.

    Args:
        str_or_iter: The input string or collection of strings to be converted.

    Returns:
        The output string or collection of strings in camelCase format.
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, camelize)

    s = str(str_or_iter if str_or_iter else '')
    if s.isupper() or s.isnumeric():
        return str_or_iter

    if len(s) != 0 and not s[:2].isupper():
        s = s[0].lower() + s[1:]

    return UNDERSCORE_RE.sub(lambda m: m.group(0)[-1].upper(), s)


def decamelize(str_or_iter: list | dict | str) -> list | dict | str:
    """Convert a string or collection of strings from camelCase to snake_case.

    Args:
        str_or_iter: The input string or collection of strings to be converted.

    Returns:
        The output string or collection of strings in snake_case format.
    """
    if isinstance(str_or_iter, (list, Mapping)):
        return _process_keys(str_or_iter, decamelize)

    s = str(str_or_iter if str_or_iter else '')
    if s.isupper() or s.isnumeric():
        return str_or_iter
    fixed_abbr = ACRONYM_RE.sub(lambda m: m.group(0).title(), s)
    return '_'.join(s for s in SPLIT_RE.split(fixed_abbr) if s).lower()


def _process_keys(str_or_iter: str | Iterable, fn: Callable) -> str | Iterable:
    """A helper function for camelize and decamelize functions.

    Args:
        str_or_iter: The input string or collection of strings to be processed.
        fn: The conversion function to apply to the input.

    Returns:
        The output.
    """
    if isinstance(str_or_iter, list):
        return [_process_keys(k, fn) for k in str_or_iter]
    if isinstance(str_or_iter, Mapping):
        return {fn(k): _process_keys(v, fn) for k, v in str_or_iter.items()}
    return str_or_iter
