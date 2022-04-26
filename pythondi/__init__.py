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

    def bind(self, interface=None, impl=None, lazy: bool = False) -> Optional[NoReturn]:
        if lazy is False:
            impl = impl()

        self._bindings[interface] = impl

    def unbind(self, interface) -> Optional[NoReturn]:
        """Unbind class"""
        try:
            self._bindings.pop(interface)
        except KeyError:
            raise InjectException(msg="Unbind exception")

    def clear_bindings(self) -> None:
        """Clear bindings"""
        self._bindings = {}

    @property
    def bindings(self) -> dict:
        """Get current bindings"""
        return self._bindings


class Container:
    _instance = None
    _provider = None

    @classmethod
    def set(cls, provider: Provider) -> None:
        """Set provider"""
        cls._provider = provider

    @classmethod
    def get(cls) -> Provider:
        """Get current provider"""
        return cls._provider

    @classmethod
    def clear(cls) -> None:
        """Clear provider"""
        cls._provider = None


def configure(provider: Provider) -> Optional[NoReturn]:
    """Configure provider to container"""
    with _LOCK:
        if Container.get():
            raise InjectException(msg="Already injected")

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
                raise InjectException(msg="Provider does not configured")

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
