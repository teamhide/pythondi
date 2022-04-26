import inspect
import threading
from functools import wraps
from typing import Optional, NoReturn

from pythondi.container import Container
from pythondi.exceptions import (
    ProviderDoesNotConfiguredException,
    AlreadyInjectedException,
)
from pythondi.provider import Provider

_LOCK = threading.RLock()


def configure(provider: Provider) -> Optional[NoReturn]:
    """Configure provider to container"""
    with _LOCK:
        if Container.get():
            raise AlreadyInjectedException

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
            if not _provider:
                raise ProviderDoesNotConfiguredException

            # Case of auto injection
            if not params:
                annotations = inspect.getfullargspec(func).annotations
                for k, v in annotations.items():
                    if v in _provider.bindings and k not in kwargs:
                        replacement = _provider.bindings[v]
                        if inspect.isclass(replacement):
                            kwargs[k] = replacement()

                        kwargs[k] = _provider.bindings[v]
            # Case of manual injection
            else:
                for k, v in params.items():
                    kwargs[k] = v()

            if inspect.iscoroutinefunction(func):
                async def _inject(*args, **kwargs):
                    return await func(*args, **kwargs)
            else:
                def _inject(*args, **kwargs):
                    return func(*args, **kwargs)

            return _inject(*args, **kwargs)
        return wrapper
    return inner_func


__all__ = [
    "Provider",
    "configure",
    "configure_after_clear",
    "inject",
]
