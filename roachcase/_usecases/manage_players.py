from typing import Iterable
from roachcase import _repositories, _entities


class ManagePlayerUseCase:
    def __init__(self, player_repository: _repositories.PlayerRepository):
        self.__player_repo = player_repository

    def list_players(self) -> Iterable[str]:
        result = [item.get_name() for item in self.__player_repo.get()]
        return result

    def add_player(self, name: str) -> None:
        player = _entities.Player(name)
        self.__player_repo.add(player)
