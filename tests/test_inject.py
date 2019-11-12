from pythondi import Provider


def test_provider_print_bindings():
    provider = Provider()
    assert provider.bindings == {}
    provider.bind(int, str)
    assert provider.bindings[int] == str


def test_provider_bind():
    provider = Provider()
    provider.bind(int, str)
    assert provider.bindings[int] == str
