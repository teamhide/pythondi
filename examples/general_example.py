from pythondi import Provider, configure, configure_after_clear, inject
from .repo import Repo, SQLRepo


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


if __name__ == '__main__':
    # There is three ways to binding classes
    # 1. Init provider without arguments
    provider = Provider()
    # Bind one by one
    provider.bind(Repo, SQLRepo)
    # Bind all at once
    provider.bind(classes={Repo: SQLRepo})

    # 2. Init provider with arguments
    provider = Provider(cls=Repo, new_cls=SQLRepo)

    # 3. Init provider with dictionary
    provider = Provider(classes={Repo: SQLRepo})

    # Inject with configure
    configure(provider=provider)

    # Or if you want to fresh inject, use `configure_after_clear`
    configure_after_clear(provider=provider)

    # Init class without arguments
    u = Usecase()
