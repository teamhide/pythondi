from pytest import raises

from pythondi import Provider, InjectException


def test_bind_class_init():
    provider = Provider(cls=int, new_cls=str)
    assert provider.bindings[int] == str


def test_bind_class_init_with_dict():
    bind = {int: str}
    provider = Provider(classes=bind)
    assert provider.bindings[int] == str


def test_bind():
    provider = Provider()
    provider.bind(int, str)
    assert provider.bindings[int] == str


def test_bind_with_classes():
    provider = Provider()
    provider.bind(classes={int: str})
    assert provider.bindings[int] == str
    provider.bind(int, dict)
    assert provider.bindings[int] == dict


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
