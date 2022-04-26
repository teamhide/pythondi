from pythondi import Container, Provider


def test_has_shared_state():
    c1 = Container
    c2 = Container
    assert c1.get() == c2.get()


def test_has_shared_state_with_instance():
    c1 = Container()
    c2 = Container()
    assert id(c1) != id(c2)
    assert c1.get() == c2.get()


def test_clear():
    Container.set(provider=Provider())
    assert Container.get() is not None
    Container.clear()
    assert Container.get() is None


def test_set():
    Container.clear()
    assert Container.get() is None
    provider = Provider()
    Container.set(provider=provider)
    assert Container.get() == provider


def test_get():
    Container.clear()
    assert Container.get() is None
    Container.set(provider=Provider())
    assert Container.get() is not None
