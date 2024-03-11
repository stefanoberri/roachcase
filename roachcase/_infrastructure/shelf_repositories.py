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
            player_names = [item.get_name() for item in current_players]
            if player.get_name() in player_names:
                raise _repositories.PlayerAlreadyExistError()
            current_players.append(player)
            db["players"] = current_players

    def get(self) -> Iterable[_entities.Player]:
        """Get players from the repository"""
        with shelve.open(self.__db_file) as db:
            if "players" not in db:
                result = []
            else:
                result = db["players"]
        return result


class ShelfGameRepository(_repositories.GameRepository):
    def __init__(self, db_file: pathlib.Path):
        self.__db_file = str(db_file)

    def add(self, game: _entities.Game) -> None:
        """Add a game to the repository"""
        with shelve.open(self.__db_file) as db:
            if "games" not in db:
                db["games"] = []

            current_games = db["games"]
            game_names = [item.get_name() for item in current_games]
            if game.get_name() in game_names:
                raise _repositories.GameAlreadyExistError()
            current_games.append(game)
            db["games"] = current_games

    def get(self) -> Iterable[_entities.Game]:
        """Get games from the repository"""
        with shelve.open(self.__db_file) as db:
            if "games" not in db:
                result = []
            else:
                result = db["games"]
        return result


class ShelfRepositoryFactory(_repositories.RepositoryFactory):
    def __init__(self, db_file: pathlib.Path):
        self.__db_file = db_file

    @functools.lru_cache()
    def build_player_repo(self) -> ShelfPlayerRepository:
        """Build a ShelfPlayerRepository"""
        result = ShelfPlayerRepository(self.__db_file)
        return result

    @functools.lru_cache()
    def build_game_repo(self) -> ShelfGameRepository:
        """Build a ShelfPlayerRepository"""
        result = ShelfGameRepository(self.__db_file)
        return result
