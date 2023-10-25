from hello.hello import say_hello
from hello2.hello import say_hello_in


def test_hello():
    assert say_hello() == 'Hello, World!'


def test_hello2():
    assert say_hello_in() == 'Hello, World!'
