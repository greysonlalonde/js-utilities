import unittest

from js_utilities.vanilla.utils import (
    add_class_props,
    add_class_state,
    add_curls,
    add_props,
    add_state,
    add_this,
    camelize,
    const,
    decamelize,
    ternary_expression,
)


class TestJsUtilities(unittest.TestCase):
    def test_camelize(self) -> None:
        self.assertEqual(camelize('hello_world'), 'helloWorld')
        self.assertEqual(
            camelize('hello_world_hello_world'), 'helloWorldHelloWorld'
        )
        self.assertEqual(camelize('HelloWorld'), 'helloWorld')

    def test_decamelize(self) -> None:
        self.assertEqual(decamelize('helloWorld'), 'hello_world')
        self.assertEqual(
            decamelize('helloWorldHelloWorld'), 'hello_world_hello_world'
        )
        self.assertEqual(decamelize('HelloWorld'), 'hello_world')

    def test_add_curls(self) -> None:
        self.assertEqual(add_curls('foo'), '{foo}')
        self.assertEqual(add_curls(''), '{}')

    def test_add_state(self) -> None:
        self.assertEqual(add_state(), 'state')
        self.assertEqual(add_state('count'), 'state.count')
        self.assertEqual(add_state(''), 'state')

    def test_add_props(self) -> None:
        self.assertEqual(add_props(), 'props')
        self.assertEqual(add_props('name'), 'props.name')
        self.assertEqual(add_props(''), 'props')

    def test_add_this(self) -> None:
        self.assertEqual(add_this(), 'this.')
        self.assertEqual(add_this('state'), 'this.state')
        self.assertEqual(add_this(''), 'this.')

    def test_add_class_props(self) -> None:
        self.assertEqual(add_class_props('name'), 'this.props.name')
        self.assertEqual(add_class_props(''), 'this.props')

    def test_add_class_state(self) -> None:
        self.assertEqual(add_class_state('count'), 'this.state.count')
        self.assertEqual(add_class_state(''), 'this.state')

    def test_const(self) -> None:
        self.assertEqual(const('MY_CONST', '10'), 'const MY_CONST = 10')
        self.assertEqual(const('MY_CONST', '"foo"'), 'const MY_CONST = "foo"')
        self.assertEqual(const('MY_CONST', 'true'), 'const MY_CONST = true')

    def test_ternary_expression(self) -> None:
        self.assertEqual(
            ternary_expression('x > 10', 5, 10), '{x > 10 ? 5 : 10}'
        )
        self.assertEqual(
            ternary_expression('x > 0', 'positive', 'negative'),
            '{x > 0 ? "positive" : "negative"}',
        )
        self.assertEqual(
            ternary_expression('x is not None', True, False),
            '{x is not None ? true : false}',
        )


if __name__ == '__main__':
    unittest.main()
