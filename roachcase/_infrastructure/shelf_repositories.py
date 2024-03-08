import functools
from typing import Iterable
import shelve
import pathlib
from roachcase import _entities, _repositories


class ShelfPlayerRepository(_repositories.PlayerRepository):
    def __init__(self, db_file: pathlib.Path):
        self.__db_file = str(db_file)

    def add(self, player: _entities.Player) -> None:
        """Add a player to the repository"""
        with shelve.open(self.__db_file) as db:
            if "players" not in db:
                db["players"] = []

            current_players = db["players"]
            current_players_names = [item.get_name() for item in current_players]
            if player.get_name() in current_players_names:
                raise _repositories.PlayerAlreadyExistError()
            current_players.append(player)
            db["players"] = [player]

    def get(self) -> Iterable[_entities.Player]:
        """Get players from the repository"""
        with shelve.open(self.__db_file) as db:
            result: Iterable[_entities.Player] = db["players"]
        return result


class ShelfRepositoryFactory(_repositories.RepositoryFactory):
    def __init__(self, db_file: pathlib.Path):
        self.__db_file = db_file

    @functools.lru_cache()
    def build_player_repo(self) -> ShelfPlayerRepository:
        """Build a ShelfPlayerRepository"""
        result = ShelfPlayerRepository(self.__db_file)
        return result
