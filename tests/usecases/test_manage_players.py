import pytest
from roachcase._usecases import factories
from roachcase import _repositories


@pytest.fixture
def usecase_factory():
    repo_factory = _repositories.InMemoryRepositoryFactory()
    result = factories.UseCaseFactory(repo_factory)
    return result


class TestManagePlayerUseCase:
    def test_list_player(self, usecase_factory):
        usecase = usecase_factory.build_manage_players()
        observed = usecase.list_players()
        assert set(observed) == set()
        usecase.add_player("Mark")
        observed = usecase.list_players()
        assert set(observed) == set(["Mark"])
        with pytest.raises(Exception):
            usecase.add_player("Mark")
