import pytest

from tests.fixtures import john, jane, football, volleyball
from tests.fixtures import in_memory_repository_factory as repo_factory
from roachcase import _entities, _repositories


class TestInMemoryPlayerRepository:
    @pytest.fixture
    def player_repo(self, repo_factory):
        result = repo_factory.build_player_repo()
        return result

    def test_round_trip(self, john, jane, player_repo):
        # if no players are added, return empty list
        observed = player_repo.get()
        assert list(observed) == []

        player_repo.add(john)
        observed = player_repo.get()
        expected = [john]
        assert list(observed) == expected

        player_repo.add(jane)
        observed = player_repo.get()
        expected = [john, jane]
        assert list(observed) == expected

    def test_adding_player_with_same_name_raises(self, john, player_repo):
        player_repo.add(john)
        with pytest.raises(_repositories.PlayerAlreadyExistError):
            player_repo.add(john)
        another_player_named_john = _entities.Player("John")
        with pytest.raises(_repositories.PlayerAlreadyExistError):
            player_repo.add(another_player_named_john)


class TestInMemoryGameRepository:
    @pytest.fixture
    def game_repo(self):
        result = _repositories.InMemoryGameRepository()
        return result

    def test_round_trip(self, football, volleyball, game_repo):
        observed = game_repo.get()
        assert list(observed) == []

        game_repo.add(football)
        observed = game_repo.get()
        expected = [football]
        assert list(observed) == expected

        game_repo.add(volleyball)
        observed = game_repo.get()
        expected = [football, volleyball]
        assert list(observed) == expected

    def test_adding_game_with_same_name_raises(self, football, game_repo):
        game_repo.add(football)
        with pytest.raises(_repositories.GameAlreadyExistError):
            game_repo.add(football)
        another_football = _entities.Game("Football")
        with pytest.raises(_repositories.GameAlreadyExistError):
            game_repo.add(another_football)


class TestInMemoryRepositoryFactory:
    def test_build_player_repo(self):
        factory = _repositories.InMemoryRepositoryFactory()
        observed = factory.build_player_repo()
        assert isinstance(observed, _repositories.InMemoryPlayerRepository)

    def test_build_game_repo(self):
        factory = _repositories.InMemoryRepositoryFactory()
        observed = factory.build_game_repo()
        assert isinstance(observed, _repositories.InMemoryGameRepository)
