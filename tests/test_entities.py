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


class TestGame:
    def test_get_name(self):
        game = _entities.Game("Volleyball")
        observed = game.get_name()
        assert observed == "Volleyball"

    def test_eq(self):
        game1 = _entities.Game("Football")
        game2 = _entities.Game("Football")
        game3 = _entities.Game("Starcraft")
        assert game1 == game1
        assert game1 == game2
        assert game2 != game3
        assert game1 != "Football"
