import inspect

import pytest

from pythondi import inject, Provider, configure_after_clear


class Repo:
    def __init__(self):
        pass


class SQLRepo:
    def __init__(self):
        pass


class Usecase:
    def __init__(self):
        pass


class UserUsecase:
    def __init__(self):
        pass


def test_sync_inject_without_parameter_lazy_is_true():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        assert not isinstance(repo, SQLRepo)

    func()


def test_sync_inject_without_parameter_lazy_is_true_singleton():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        return repo

    @inject()
    def func2(repo: Repo):
        return repo

    repo1 = func()
    repo2 = func2()

    assert repo1 == repo2
    assert inspect.isclass(repo1)
    assert inspect.isclass(repo2)


def test_sync_inject_without_parameter_lazy_is_false():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    func()


def test_sync_inject_without_parameter_lazy_is_false_singleton():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        return repo

    @inject()
    def func2(repo: Repo):
        return repo

    repo1 = func()
    repo2 = func2()

    assert repo1 == repo2
    assert not inspect.isclass(repo1)
    assert not inspect.isclass(repo2)


def test_sync_inject_without_parameter_multiple_bind_lazy_true():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    provider.bind(Usecase, UserUsecase, lazy=True)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo, usecase: Usecase):
        assert not isinstance(repo, SQLRepo)
        assert not isinstance(usecase, UserUsecase)

    func()


def test_sync_inject_without_parameter_multiple_bind_lazy_false():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    provider.bind(Usecase, UserUsecase, lazy=False)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo, usecase: Usecase):
        assert isinstance(repo, SQLRepo)
        assert isinstance(usecase, UserUsecase)

    func()


def test_sync_inject_with_parameter():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure_after_clear(provider)

    @inject(repo=SQLRepo)
    def func(repo):
        assert isinstance(repo, SQLRepo)

    func()


def test_sync_inject_with_parameter_multiple_bind():
    provider = Provider()
    configure_after_clear(provider)

    @inject(repo=SQLRepo, usecase=UserUsecase)
    def func(repo, usecase):
        assert isinstance(repo, SQLRepo)
        assert isinstance(usecase, UserUsecase)

    func()


@pytest.mark.asyncio
async def test_async_inject_without_parameter_lazy_true():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo):
        assert not isinstance(repo, SQLRepo)

    await func()


@pytest.mark.asyncio
async def test_async_inject_without_parameter_lazy_false():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    await func()


@pytest.mark.asyncio
async def test_async_inject_without_parameter_multiple_bind_lazy_true():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=True)
    provider.bind(Usecase, UserUsecase, lazy=True)
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo, usecase: Usecase):
        assert not isinstance(repo, SQLRepo)
        assert not isinstance(usecase, UserUsecase)

    await func()


@pytest.mark.asyncio
async def test_async_inject_without_parameter_multiple_bind_lazy_false():
    provider = Provider()
    provider.bind(Repo, SQLRepo, lazy=False)
    provider.bind(Usecase, UserUsecase, lazy=False)
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo, usecase: Usecase):
        assert isinstance(repo, SQLRepo)
        assert isinstance(usecase, UserUsecase)

    await func()


@pytest.mark.asyncio
async def test_async_inject_with_parameter():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure_after_clear(provider)

    @inject(repo=SQLRepo)
    async def func(repo):
        assert isinstance(repo, SQLRepo)

    await func()


@pytest.mark.asyncio
async def test_async_inject_with_parameter_multiple_bind():
    provider = Provider()
    configure_after_clear(provider)

    @inject(repo=SQLRepo, usecase=UserUsecase)
    async def func(repo, usecase):
        assert isinstance(repo, SQLRepo)
        assert isinstance(usecase, UserUsecase)

    await func()
