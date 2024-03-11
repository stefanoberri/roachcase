import abc
import functools
from typing import Iterable, List
from roachcase import _entities


class PlayerAlreadyExistError(ValueError):
    pass


class GameAlreadyExistError(ValueError):
    pass


class PlayerRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, player: _entities.Player) -> None:
        """Add a player to the repository"""

    @abc.abstractmethod
    def get(self) -> Iterable[_entities.Player]:
        """Get players from the repository"""


class InMemoryPlayerRepository(PlayerRepository):
    """An implementation of PlayerRepository that stores players in memory"""

    def __init__(self) -> None:
        self.__store: List[_entities.Player] = []

    def add(self, player: _entities.Player) -> None:
        names = [item.get_name() for item in self.__store]
        if player.get_name() in names:
            raise PlayerAlreadyExistError()
        self.__store.append(player)

    def get(self) -> Iterable[_entities.Player]:
        return iter(self.__store)


class GameRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, game: _entities.Game) -> None:
        """Add a game to the repository"""

    @abc.abstractmethod
    def get(self) -> Iterable[_entities.Game]:
        """Get players from the repository"""


class InMemoryGameRepository(GameRepository):
    """An implementation of GameRepository that stores games in memory"""

    def __init__(self) -> None:
        self.__store: List[_entities.Game] = []

    def add(self, game: _entities.Game) -> None:
        """Add a game to the repository"""
        names = [item.get_name() for item in self.__store]
        if game.get_name() in names:
            raise GameAlreadyExistError()
        self.__store.append(game)

    def get(self) -> Iterable[_entities.Game]:
        """Get players from the repository"""
        return iter(self.__store)


class RepositoryFactory(abc.ABC):
    @abc.abstractmethod
    def build_player_repo(self) -> PlayerRepository:
        """Build a PlayerRepository"""

    @abc.abstractmethod
    def build_game_repo(self) -> GameRepository:
        """Build a PlayerRepository"""


class InMemoryRepositoryFactory(RepositoryFactory):
    @functools.lru_cache()
    def build_player_repo(self) -> InMemoryPlayerRepository:
        """Build an InMemoryPlayerRepository"""
        result = InMemoryPlayerRepository()
        return result

    @functools.lru_cache()
    def build_game_repo(self) -> InMemoryGameRepository:
        """Build an InMemoryGameRepository"""
        result = InMemoryGameRepository()
        return result
