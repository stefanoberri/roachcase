from roachcase._usecases import factories
from roachcase._usecases import manage_players


class TestUseCaseFactory:
    def test_build_manage_players(self):
        factory = factories.UseCaseFactory()
        observed = factory.build_manage_players()
        assert isinstance(observed, manage_players.ManagePlayerUseCase)
        # the factory is a singleton
        reobserved = factory.build_manage_players()
        assert observed == reobserved
