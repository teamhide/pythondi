from pythondi import Provider, configure, configure_after_clear, inject
from .repo import Repo, SQLRepo


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


if __name__ == '__main__':
    # Init provider
    provider = Provider()

    # Bind `Impl` class to `Interface` class
    provider.bind(Repo, SQLRepo)

    # Inject with configure
    configure(provider=provider)

    # Or if you want to fresh inject, use `configure_after_clear`
    configure_after_clear(provider=provider)

    # Init class without arguments
    u = Usecase()
