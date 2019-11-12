# Python Dependency Injection Library

## Usage

1. Add injection policy

```python
from pythondi import Provider, configure


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


if __name__ == '__main__':
    di = DI()
    di.bind_and_configure()

```

2. Import inject

```python
from pythondi import inject
```

3. Add type annotations that you want to inject dependencies

```python
class Usecase:
    def __init__(self, repo: Repo):
        self.repo = repo
```

4. Add decorator

```python
class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo
```

5. Initialize class with no arguments

```python
usecase = Usecase()
```

Or, you can also inject manually through decorator arguments

```python
class Usecase:
    @inject(repo=SQLRepo)
    def __init__(self, repo):
        self.repo = repo
```

In this case, do not have to configure providers and type annotation.