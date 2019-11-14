from pythondi import Container, Provider


def test_singleton():
    c1 = Container
    c2 = Container
    assert id(c1) == id(c2)


def test_clear():
    Container.set(provider=Provider())
    assert Container.get() != {}
    Container.clear()
    assert Container.get() == {}


def test_set():
    Container.clear()
    assert Container.get() == {}
    provider = Provider()
    Container.set(provider=provider)
    assert Container.get() == provider


def test_get():
    Container.clear()
    assert Container.get() == {}
    Container.set(provider=Provider())
    assert Container.get() != {}
