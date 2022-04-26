from pytest import raises

from pythondi import Provider, InjectException
import inspect


class Repo:
    def __init__(self):
        pass


class SQLRepo:
    def __init__(self):
        pass


def test_bind_lazy_is_true():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    assert provider.bindings[Repo] == SQLRepo
    assert inspect.isclass(provider.bindings[Repo])


def test_bind_lazy_is_false():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    assert provider.bindings[Repo] != SQLRepo
    assert not inspect.isclass(provider.bindings[Repo])


def test_unbind():
    provider = Provider()
    with raises(InjectException):
        provider.unbind(interface=int)

    provider.bind(int, str)
    provider.unbind(interface=int)
    assert provider.bindings == {}


def test_clear_bindings():
    provider = Provider()
    provider.bind(int, str)
    provider.bind(list, dict)
    provider.clear_bindings()
    assert provider.bindings == {}
