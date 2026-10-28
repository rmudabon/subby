from types import SimpleNamespace


def fake_user(fake_id: int):
    return SimpleNamespace(id=fake_id)
