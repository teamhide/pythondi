import inspect
import threading
from functools import wraps
from typing import Optional, NoReturn

_LOCK = threading.RLock()


class InjectException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class Provider:
    def __init__(self):
        self._bindings = {}

    def bind(self, cls, new_cls) -> None:
        """Bind class to another class"""
        self._bindings[cls] = new_cls

    def unbind(self, cls) -> None:
        """Unbind class"""
        try:
            self._bindings.pop(cls)
        except KeyError:
            raise InjectException(msg='Unbind exception')

    def clear_bindings(self) -> None:
        """Clear bindings"""
        self._bindings = {}

    @property
    def bindings(self) -> dict:
        """Get current bindings"""
        return self._bindings


class Container:
    """Singleton container class"""
    _instance = None
    _provider = None

    def __new__(cls, *args, **kwargs):
        if not Container._instance:
            Container._instance = super().__new__(cls, *args, **kwargs)
        return Container._instance

    @classmethod
    def set(cls, provider: Provider):
        """Set provider"""
        cls._provider = provider

    @classmethod
    def get(cls):
        """Get current provider"""
        return cls._provider

    @classmethod
    def clear(cls):
        """Clear provider"""
        cls._provider = {}


def configure(provider: Provider) -> Optional[NoReturn]:
    """Configure provider to container"""
    with _LOCK:
        if Container.get():
            raise InjectException(msg='Already injected')

    with _LOCK:
        Container.set(provider=provider)


def configure_after_clear(provider: Provider) -> None:
    """Clear existing provider and configure new provider"""
    with _LOCK:
        if Container.get():
            clear()

        Container.set(provider=provider)


def clear() -> None:
    """Clear current provider"""
    _container = Container

    with _LOCK:
        _container.clear()


def inject(**params):
    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _provider = Container.get()

            # Case of auto injection
            if params == {}:
                annotations = inspect.getfullargspec(func).annotations
                for k, v in annotations.items():
                    if v in _provider.bindings:
                        kwargs[k] = _provider.bindings[v]()
            # Case of manual injection
            else:
                for k, v in params.items():
                    kwargs[k] = v()
            func(*args, **kwargs)
        return wrapper
    return inner_func
