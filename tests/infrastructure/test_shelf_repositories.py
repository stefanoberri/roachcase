import pytest

from roachcase._infrastructure import shelf_repositories
from tests import test_repositories
from tests.fixtures import john, jane, football, volleyball


@pytest.fixture
def shelf_repo_factory(tmp_path):
    db = tmp_path / "shelf.db"
    result = shelf_repositories.ShelfRepositoryFactory(db)
    return result


class TestShelfPlayerRepository(test_repositories.TestInMemoryPlayerRepository):
    """The same test for the in memory repository should also pass the
    shelf repository."""

    @pytest.fixture
    def repo(self, shelf_repo_factory):
        result = shelf_repo_factory.build_player_repo()
        return result

    def test_round_trip(self, john, jane, repo):
        super().test_round_trip(john, jane, repo)

    def test_adding_player_with_same_name_raises(self, john, repo):
        super().test_adding_player_with_same_name_raises(john, repo)


class TestShelfGameRepository(test_repositories.TestInMemoryGameRepository):
    """The same test for the in memory repository should also pass the
    shelf repository."""

    @pytest.fixture
    def repo(self, tmp_path):
        db = tmp_path / "shelf.db"
        result = shelf_repositories.ShelfGameRepository(db)
        return result

    def test_round_trip(self, football, volleyball, repo):
        super().test_round_trip(football, volleyball, repo)

    def test_adding_game_with_same_name_raises(self, football, repo):
        super().test_adding_game_with_same_name_raises(football, repo)


class TestShelfRepositoryFactory:
    def test_build_player_repo(self, tmp_path):
        factory = shelf_repositories.ShelfRepositoryFactory(tmp_path)
        observed = factory.build_player_repo()
        assert isinstance(observed, shelf_repositories.ShelfPlayerRepository)

    def test_build_game_repo(self, tmp_path):
        factory = shelf_repositories.ShelfRepositoryFactory(tmp_path)
        observed = factory.build_game_repo()
        assert isinstance(observed, shelf_repositories.ShelfGameRepository)
