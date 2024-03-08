from roachcase import _entities


class TestPlayer:
    def test_get_name(self):
        player = _entities.Player("John")
        observed = player.get_name()
        assert observed == "John"

    def test_eq(self):
        player1 = _entities.Player("John")
        player2 = _entities.Player("John")
        player3 = _entities.Player("Mark")
        assert player1 == player1
        assert player1 == player2
        assert player2 != player3
        assert player1 != "John"
