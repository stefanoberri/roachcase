from typing import Iterable
from roachcase import _repositories, _entities


class ManageGameUseCase:
    def __init__(self, game_repository: _repositories.GameRepository):
        self.__game_repo = game_repository

    def list_games(self) -> Iterable[str]:
        result = [item.get_name() for item in self.__game_repo.get()]
        return result

    def add_game(self, name: str) -> None:
        game = _entities.Game(name)
        self.__game_repo.add(game)
