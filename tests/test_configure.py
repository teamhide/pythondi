from pytest import raises
from pythondi import Container

from pythondi import (
    configure,
    configure_after_clear,
    Provider,
    InjectException,
    Container,
)


class Repo:
    def __init__(self):
        pass


class SQLRepo:
    def __init__(self):
        pass


def test_configure_lazy_is_true():
    Container.clear()
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    configure(provider=provider)
    assert isinstance(Container.get(), Provider)
    assert Container.get().bindings[Repo] == SQLRepo
    with raises(InjectException):
        configure(provider=provider)
    Container.clear()


def test_configure_lazy_is_false():
    Container.clear()
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    configure(provider=provider)
    assert isinstance(Container.get(), Provider)
    assert Container.get().bindings[Repo] != SQLRepo
    with raises(InjectException):
        configure(provider=provider)
    Container.clear()


def test_configure_after_clear_lazy_is_true():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    configure_after_clear(provider=provider)

    provider = Provider()
    provider.bind(SQLRepo, Repo, lazy=True)
    configure_after_clear(provider=provider)
    with raises(KeyError):
        assert isinstance(Container.get(), Provider)
        assert Container.get().bindings[Repo] == SQLRepo


def test_configure_after_clear_lazy_is_false():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    configure_after_clear(provider=provider)

    provider = Provider()
    provider.bind(SQLRepo, Repo, lazy=False)
    configure_after_clear(provider=provider)
    with raises(KeyError):
        assert isinstance(Container.get(), Provider)
        assert Container.get().bindings[Repo] != SQLRepo
