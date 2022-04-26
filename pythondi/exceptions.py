class AlreadyInjectedException(Exception):
    def __init__(self):
        super().__init__("Already injected")


class ProviderDoesNotConfiguredException(Exception):
    def __init__(self):
        super().__init__("Provider does not configured")


class DoesNotBoundException(Exception):
    def __init__(self, cls_name):
        super().__init__(f"{cls_name} is not bound")
