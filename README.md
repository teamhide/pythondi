# pythondi
[![license]](/LICENSE)
[![pypi]](https://pypi.org/project/pythondi/)
[![pyversions]](http://pypi.python.org/pypi/pythondi)
![badge](https://action-badges.now.sh/teamhide/pythondi)
[![Downloads](https://pepy.tech/badge/pythondi)](https://pepy.tech/project/pythondi)

---

pythondi is a lightweight dependency injection library for python

Support both sync and async functions

## Installation

```python
pip3 install pythondi
```

## Usage

First, you have to binding classes to provider.

There is three different ways to binding.

- Binding one by one

```python
from pythondi import Provider


provider = Provider()
provider.bind(Repo, SQLRepo)
provider.bind(Usecase, CreateUsecase)
```

- Binding at initialization

```python
from pythondi import Provider


provider = Provider(cls=Repo, new_cls=SQLRepo)
```

- Binding at initialization with dictionary

```python
from pythondi import Provider


provider = Provider(classes={Repo: SQLRepo, Usecase: CreateUsecase})
```


After binding, you need to configure it to container

```python
from pythondi import configure, configure_after_clear


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

## For test

In case of test codes, you probably want to use mock objects.

In that case, you must use keyword arguments.

```python
class MockRepo:
    pass


@inject()
def test(repo: Repo):
    return repo
```

**Yes:**
```python
test(repo=MockRepo())
```

**No:**
```python
test(MockRepo())
test(MockRepo)
```

## Note

At the moment of inject, class is automatically initialized.

So you don't have to initialize your class inside of code.

**Yes:**
```python
@inject()
def __init__(self, repo: Repo):
    self.repo = repo
```

**No:**
```python
@inject()
def __init__(self, repo: Repo):
    self.repo = repo()
```

## General example

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

    # Or if you want to fresh injection, use `configure_after_clear`
    configure_after_clear(provider=provider)

    # Init class without arguments
    u = Usecase()
```

## FastAPI example

```python
from fastapi import FastAPI, APIRouter

from pythondi import Provider, configure, inject
import abc

router = APIRouter()


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


@router.route('/')
def home():
    usecase = Usecase()
    usecase.repo.get()
    return {'hello': 'world'}


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


def create_app():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure(provider=provider)
    app = FastAPI()
    app.include_router(router)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

## Flask example

```python
from flask import Flask, Blueprint, jsonify

from pythondi import Provider, configure, inject
import abc

bp = Blueprint('home', __name__)


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


@bp.route('/')
def home():
    usecase = Usecase()
    usecase.repo.get()
    return jsonify({'hello': 'world'})


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


def create_app():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure(provider=provider)
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
```

## Sanic example
```python
import abc

from sanic import Sanic, Blueprint
from sanic.response import json

from pythondi import Provider, configure, inject


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


bp = Blueprint('home', url_prefix='/')


@bp.route('/')
async def home(request):
    usecase = Usecase()
    usecase.repo.get()
    return json({'hello': 'world'})


class Usecase:
    @inject()
    def __init__(self, repo: Repo):
        self.repo = repo


def create_app():
    provider = Provider()
    provider.bind(Repo, SQLRepo)
    configure(provider=provider)
    app = Sanic(__name__)
    app.blueprint(bp)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

```

## Django example

```python
"""
In case of django, just put the initializing code inside of django startup

You can use project folder's __init__.py or urls.py
"""
```
[license]: https://img.shields.io/badge/License-Apache%202.0-blue.svg
[pypi]: https://img.shields.io/pypi/v/pythondi
[pyversions]: https://img.shields.io/pypi/pyversions/pythondi
