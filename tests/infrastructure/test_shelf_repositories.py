import pytest

from roachcase._infrastructure import shelf_repositories
from tests import test_repositories
from tests.fixtures import john


class TestShelfPlayerRepository(test_repositories.TestInMemoryPlayerRepository):
    """The same test for the in memory repository should also pass the
    shelf repository."""

    @pytest.fixture
    def repo(self, tmp_path):
        db = tmp_path / "shelf.db"
        result = shelf_repositories.ShelfPlayerRepository(db)
        return result

    def test_round_trip(self, john, repo):
        super().test_round_trip(john, repo)

    def test_adding_player_with_same_name_raises(self, john, repo):
        super().test_adding_player_with_same_name_raises(john, repo)


class TestShelfRepositoryFactory:
    def test_build_player_repo(self, tmp_path):
        factory = shelf_repositories.ShelfRepositoryFactory(tmp_path)
        observed = factory.build_player_repo()
        assert isinstance(observed, shelf_repositories.ShelfPlayerRepository)
