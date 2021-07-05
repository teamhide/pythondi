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


def test_sync_inject_without_parameter():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    func()


def test_sync_inject_without_parameter_multiple_bind():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    provider.bind(Usecase, UserUsecase)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo, usecase: Usecase):
        assert isinstance(repo, SQLRepo)
        assert isinstance(usecase, UserUsecase)

    func()


def test_sync_inject_with_classes_argument():
    provider = Provider()
    provider.bind(classes={Repo: SQLRepo})
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    func()


def test_sync_inject_with_classes_argument_multiple_bind():
    provider = Provider()
    provider.bind(classes={Repo: SQLRepo, Usecase: UserUsecase})
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
async def test_async_inject_without_parameter():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    await func()


@pytest.mark.asyncio
async def test_async_inject_without_parameter_multiple_bind():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    provider.bind(Usecase, UserUsecase)
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo, usecase: Usecase):
        assert isinstance(repo, SQLRepo)
        assert isinstance(usecase, UserUsecase)

    await func()


@pytest.mark.asyncio
async def test_async_inject_with_classes_argument():
    provider = Provider()
    provider.bind(classes={Repo: SQLRepo})
    configure_after_clear(provider)

    @inject()
    async def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    await func()


@pytest.mark.asyncio
async def test_async_inject_with_classes_argument_multiple_bind():
    provider = Provider()
    provider.bind(classes={Repo: SQLRepo, Usecase: UserUsecase})
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


@pytest.mark.asyncio
async def test_manual_provide_args_outside():
    provider = Provider()
    provider.bind(classes={Repo: SQLRepo})
    configure_after_clear(provider)

    class MockRepo:
        pass

    @inject()
    async def func(repo: Repo):
        return repo

    result = await func(repo=MockRepo())
    assert isinstance(result, MockRepo)
