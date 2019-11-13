# Python Dependency Injection Library

## Installation

```python
pip3 install pythondi
```

## Usage

Add injection policy

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

Import inject

```python
from pythondi import inject
```

Add type annotations that you want to inject dependencies

```python
class Usecase:
    def __init__(self, repo: Repo):
        self.repo = repo
```

Add decorator

```python
class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo
```

Initialize class with no arguments

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

**Note**

At the moment of inject, class is automatically initialized.

So you don't have to initialize your class inside of code.

Yes:
```python
def __init__(self, repo: Repo):
    self.repo = repo
```

No:
```python
def __init__(self, repo: Repo):
    self.repo = repo()
```

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