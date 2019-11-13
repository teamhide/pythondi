import inspect
import threading
from functools import wraps
from typing import Optional, NoReturn

_PROVIDER = None
_LOCK = threading.RLock()


class Provider:
    def __init__(self):
        self._bindings = {}

    def bind(self, cls, new_cls) -> None:
        """Binding class to another class"""
        self._bindings[cls] = new_cls

    def unbind(self, cls) -> None:
        """Unbinding class"""
        self._bindings.pop(cls)

    def clear_bindings(self) -> None:
        """Clear bindings"""
        self._bindings = {}

    @property
    def bindings(self) -> dict:
        """Return current binding classes"""
        return self._bindings


def configure(provider: Provider) -> Optional[NoReturn]:
    """Configure provider"""
    global _PROVIDER

    if _PROVIDER:
        raise Exception('Already injected')

    with _LOCK:
        _PROVIDER = provider


def configure_after_clear(provider: Provider) -> None:
    """Clear existing provider and configure new provider"""
    global _PROVIDER

    if _PROVIDER:
        clear()

    with _LOCK:
        _PROVIDER = provider


def clear(provider: Provider = None) -> None:
    global _PROVIDER

    with _LOCK:
        _PROVIDER = None

    if provider:
        provider.clear_bindings()


def inject(**params):
    def inner_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Case of auto injection
            if params == {}:
                annotations = inspect.getfullargspec(func).annotations
                for k, v in annotations.items():
                    if v in _PROVIDER.bindings:
                        kwargs[k] = _PROVIDER.bindings[v]()
            # Case of manual injection
            else:
                for k, v in params.items():
                    kwargs[k] = v()
            func(*args, **kwargs)
        return wrapper
    return inner_func
