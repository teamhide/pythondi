from pythondi import inject, Provider, configure_after_clear


class Repo:
    def __init__(self):
        pass


class SQLRepo:
    def __init__(self):
        pass


def test_inject_without_parameter():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure_after_clear(provider)

    @inject()
    def func(repo: Repo):
        assert isinstance(repo, SQLRepo)

    func()


def test_inject_with_parameter():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure_after_clear(provider)

    @inject(repo=SQLRepo)
    def func(repo):
        assert isinstance(repo, SQLRepo)

    func()
