import unittest

from js_utilities.react.base_components import ReactComponent
from js_utilities.react.utils import (
    _render_return,
    class_declaration,
    react_component,
    react_function,
)


class TestUtils(unittest.TestCase):
    def test_react_function(self):
        # Test with a function that starts with "use_"
        def use_state():
            var = react_function()
            return var

        self.assertEqual(use_state(), 'React.useState()')

        def use_effect():
            var = react_function()
            return var

        # Test with a function that starts with "useEffect_"
        self.assertEqual(use_effect(), 'React.useEffect()')

    def test_render_return(self):
        # Test with one component
        self.assertEqual(
            _render_return('ComponentA'),
            'render(){return (<ComponentA />)}',
        )

        # Test with multiple components
        self.assertEqual(
            _render_return('ComponentB'),
            'render(){return (<ComponentB />)}',
        )

    def test_class_declaration(self):
        # Test with a functional component
        self.assertEqual(
            class_declaration('MyComponent', 'function'),
            'export class MyComponent extends React.Function',
        )

        # Test with a class component
        self.assertEqual(
            class_declaration('MyComponent', 'component'),
            'export class MyComponent extends React.Component',
        )

    def test_react_component(self):
        # Test with a functional component
        app = ReactComponent(name='App', type='div')
        self.assertRaises(NotImplementedError, react_component, app)

        home = ReactComponent(name='Home', props={'count': 0}, type='div')
        self.assertRaises(NotImplementedError, react_component, home)


if __name__ == '__main__':
    unittest.main()
