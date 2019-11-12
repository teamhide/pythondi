# Python Dependency Injection Library

## Usage

1. Add injection policy

```python
from pythondi import Provider, configure, configure_after_clear


# Init provider
provider = Provider()

# Bind `Impl` class to `Interface` class
provider.bind(Repo, SQLRepo)

# Inject with configure
configure(provider=provider)

# Or if you want to fresh inject, use `configure_after_clear`
configure_after_clear(provider=provider)
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

**Full Example**

```python
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
    print(u.__dict__)
```