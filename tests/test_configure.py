from pytest import raises

from pythondi import (
    configure,
    configure_after_clear,
    Provider,
    InjectException
)


def test_configure():
    provider = Provider()
    provider.bind(int, str)
    configure(provider=provider)
    from pythondi import _PROVIDER
    assert isinstance(_PROVIDER, Provider)
    assert _PROVIDER.bindings[int] == str


def test_configure_after_clear():
    _PROVIDER = None
    provider = Provider()
    provider.bind(int, str)
    with raises(InjectException):
        configure(provider=provider)

    provider = Provider()
    provider.bind(str, int)
    from pythondi import _PROVIDER
    configure_after_clear(provider=provider)
    assert isinstance(_PROVIDER, Provider)
    assert _PROVIDER.bindings[int] == str

