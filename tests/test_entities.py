from roachcase import _entities


class TestPlayer:
    def test_get_name(self):
        player = _entities.Player("John")
        observed = player.get_name()
        assert observed == "John"
