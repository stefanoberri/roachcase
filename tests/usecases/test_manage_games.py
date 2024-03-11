import pytest
from roachcase._usecases import factories
from roachcase import _repositories


@pytest.fixture
def usecase_factory():
    repo_factory = _repositories.InMemoryRepositoryFactory()
    result = factories.UseCaseFactory(repo_factory)
    return result


class TestManagePlayerUseCase:
    def test_list_game(self, usecase_factory):
        usecase = usecase_factory.build_manage_games()
        observed = usecase.list_games()
        assert set(observed) == set()
        usecase.add_game("Football")
        observed = usecase.list_games()
        assert set(observed) == set(["Football"])
        with pytest.raises(Exception):
            usecase.add_game("Football")
