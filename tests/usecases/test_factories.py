from roachcase._usecases import factories
from roachcase._usecases import manage_players
from roachcase import _repositories


class TestUseCaseFactory:
    def test_build_manage_players(self):
        repository_factory = _repositories.InMemoryRepositoryFactory()
        factory = factories.UseCaseFactory(repository_factory)
        observed = factory.build_manage_players()
        assert isinstance(observed, manage_players.ManagePlayerUseCase)
        # the factory is a singleton
        reobserved = factory.build_manage_players()
        assert observed == reobserved

    def test_set_get_repo_factory(self):
        repository_factory = _repositories.InMemoryRepositoryFactory()
        factory = factories.UseCaseFactory(repository_factory)
        observed = factory.get_repo_factory()
        assert observed == repository_factory
        new_repository_factory = _repositories.InMemoryRepositoryFactory()
        factory.set_repo_factory(new_repository_factory)
        observed = factory.get_repo_factory()
        assert observed == new_repository_factory
