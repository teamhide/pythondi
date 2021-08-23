from pytest import raises

from pythondi import (
    configure,
    configure_after_clear,
    Provider,
    InjectException,
    Container,
)


def test_configure():
    provider = Provider()
    provider.bind(int, str)
    configure(provider=provider)
    assert isinstance(Container.get(), Provider)
    assert Container.get().bindings[int] == str
    with raises(InjectException):
        configure(provider=provider)
    Container.clear()


def test_configure_after_clear():
    provider = Provider()
    provider.bind(int, str)
    configure_after_clear(provider=provider)

    provider = Provider()
    provider.bind(str, int)
    configure_after_clear(provider=provider)
    assert isinstance(Container.get(), Provider)
    assert Container.get().bindings[str] == int
