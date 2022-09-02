from pythondi.exceptions import DoesNotBoundException


class Provider:
    def __init__(self):
        self._bindings = {}

    def bind(self, interface=None, impl=None, lazy: bool = False) -> None:
        if lazy is False:
            impl = impl()

        self._bindings[interface] = impl

    def unbind(self, interface) -> None:
        """Unbind class"""
        try:
            self._bindings.pop(interface)
        except KeyError:
            raise DoesNotBoundException(cls_name=interface.__class__.__name__)

    def clear_bindings(self) -> None:
        """Clear bindings"""
        self._bindings = {}

    @property
    def bindings(self) -> dict:
        """Get current bindings"""
        return self._bindings
