from pytest import raises

from pythondi import Provider, InjectException


def test_bind():
    provider = Provider()
    provider.bind(int, str)
    assert provider.bindings[int] == str


def test_unbind():
    provider = Provider()
    with raises(InjectException):
        provider.unbind(cls=int)

    provider.bind(int, str)
    provider.unbind(cls=int)
    assert provider.bindings == {}


def test_clear_bindings():
    provider = Provider()
    provider.bind(int, str)
    provider.bind(list, dict)
    provider.clear_bindings()
    assert provider.bindings == {}
