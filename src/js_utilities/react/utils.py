"""This module provides utility functions for working with React components in JavaScript.

Functions:

    react_function():
        Returns a string representation of a React function call based on the name of the calling function.

    _render_return(components: str) -> str:
        Returns the render function with the given components.

    class_declaration(name: str, react_type: str) -> str:
        Returns a string representing the declaration of a JavaScript class for a given React component.

    react_component(component: ReactComponent) -> str:
        Returns a React component based on the type of the given component.
"""
from inspect import stack

from js_utilities.react.base_components import ReactComponent
from js_utilities.vanilla.utils import (
    add_curls,
    camelize,
    class_component,
    functional_component,
    return_,
)


def react_function() -> str:
    """Returns a string representation of a React function call based on the name of the calling function.

    Returns:
        A string representing a React function call.

    Examples:
        If the calling function is `use_state_hook()`, this function will return "React.useStateHook()".
    """
    action, *hook = stack()[1][3].split('_')
    if len(hook) > 1:
        hook = [word.title() for word in hook]
    hook = camelize(''.join(hook))
    return f'React.{action}{hook.title()}()'


def _render_return(components: str) -> str:
    """Returns the render function with the given components.

    Args:
        components: A string of components.

    Examples:
        >>> _render_return('ComponentA, ComponentB')
        'render() {return (<ComponentA />, <ComponentB />)}'

    Returns:
        A string representing the render function with the given components.
    """
    components = f'<{components} />'
    return f'render(){add_curls(return_(components))}'


def class_declaration(name: str, react_type: str) -> str:
    """Returns a string representing the declaration of a JavaScript class for a given React component.

    Args:
        name: The name of the class.
        react_type: The type of the React component, such as 'function' or 'component'.

    Examples:
        >>> from js_utilities.react.utils import class_declaration
        >>> class_declaration('MyComponent', 'component')
        'export class MyComponent extends React.Component'

    Returns:
        A string representing the JavaScript class declaration.
    """
    if not name.title():
        name = name.title()

    return f'export class {name} extends React.{react_type.title()}'


def react_component(component: ReactComponent) -> str:
    """Returns a React component based on the type of the given component.

    Args:
        component: The python object rendition of the javascript component to be rendered.

    Returns:
        The React component as a string.

    Examples:
        >>> from js_utilities.react.utils import react_component
        >>> from js_utilities.react.base_components import ReactComponent
        >>> app = ReactComponent()
        >>> react_component
        'class RootComponent extends React.Component { ... }'
    """
    if component.get('is_functional'):
        return functional_component(component)

    return class_component(component)
