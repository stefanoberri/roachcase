from roachcase import _repositories
from roachcase._usecases import manage_players, manage_games


class UseCaseFactory:
    """Build use cases"""

    def __init__(self, repository_factory: _repositories.RepositoryFactory):
        self.__repo_factory = repository_factory

    def get_repo_factory(self) -> _repositories.RepositoryFactory:
        return self.__repo_factory

    def set_repo_factory(
        self, repository_factory: _repositories.RepositoryFactory
    ) -> None:
        self.__repo_factory = repository_factory

    def build_manage_players(self) -> manage_players.ManagePlayerUseCase:
        player_repository = self.__repo_factory.build_player_repo()
        result = manage_players.ManagePlayerUseCase(player_repository)
        return result

    def build_manage_games(self) -> manage_games.ManageGameUseCase:
        game_repository = self.__repo_factory.build_game_repo()
        result = manage_games.ManageGameUseCase(game_repository)
        return result
