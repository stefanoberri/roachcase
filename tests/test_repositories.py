import pytest

from tests.fixtures import john
from tests.fixtures import in_memory_repository as repo
from roachcase import _entities, _repositories


class TestInMemoryPlayerRepository:
    def test_round_trip(self, john, repo):
        # if no players are added, return empty list
        observed = repo.get()
        assert list(observed) == []

        repo.add(john)
        observed = repo.get()
        expected = [john]
        assert list(observed) == expected

    def test_adding_player_with_same_name_raises(self, john, repo):
        repo.add(john)
        with pytest.raises(_repositories.PlayerAlreadyExistError):
            repo.add(john)
        another_player_named_john = _entities.Player("John")
        with pytest.raises(_repositories.PlayerAlreadyExistError):
            repo.add(another_player_named_john)
