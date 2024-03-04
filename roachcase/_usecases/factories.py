import functools
from roachcase import _repositories
from roachcase._usecases import manage_players


class UseCaseFactory:
    """Build use cases"""

    @functools.lru_cache()
    def build_manage_players(self) -> manage_players.ManagePlayerUseCase:
        player_repository = _repositories.InMemoryPlayerRepository()
        result = manage_players.ManagePlayerUseCase(player_repository)
        return result
