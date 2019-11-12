import abc

from pythondi import Provider, configure, configure_after_clear, inject


class Repo:
    """Interface class"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get(self):
        pass


class SQLRepo(Repo):
    """Impl class"""
    def __init__(self):
        pass

    def get(self):
        print('SQLRepo')


class DI:
    def __init__(self):
        self.provider = Provider()

    def bind_to_provider(self) -> None:
        # Inject `Impl` class to `Interface` class
        self.provider.bind(Repo, SQLRepo)

    def bind_and_configure(self) -> None:
        # Binding provider
        self.bind_to_provider()

        # Configure injector
        configure(provider=self.provider)

        # Configure injector after clear provider
        configure_after_clear(provider=self.provider)


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


if __name__ == '__main__':
    di = DI()
    di.bind_and_configure()
    u = Usecase()
    print(u.__dict__)
