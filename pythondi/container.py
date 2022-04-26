from pythondi.provider import Provider


class Container:
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
