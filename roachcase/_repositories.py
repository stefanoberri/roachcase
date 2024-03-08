import abc
import functools
from typing import Iterable, List
from roachcase import _entities


class PlayerAlreadyExistError(ValueError):
    pass


class PlayerRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, player: _entities.Player) -> None:
        """Add a player to the repository"""

    @abc.abstractmethod
    def get(self) -> Iterable[_entities.Player]:
        """Get players from the repository"""


class RepositoryFactory(abc.ABC):
    @abc.abstractmethod
    def build_player_repo(self) -> PlayerRepository:
        """Build a PlayerRepository"""


class InMemoryPlayerRepository(PlayerRepository):
    def __init__(self) -> None:
        self.__store: List[_entities.Player] = []

    def add(self, player: _entities.Player) -> None:
        names = [item.get_name() for item in self.__store]
        if player.get_name() in names:
            raise PlayerAlreadyExistError()
        self.__store.append(player)

    def get(self) -> Iterable[_entities.Player]:
        return iter(self.__store)


class InMemoryRepositoryFactory(RepositoryFactory):
    @functools.lru_cache()
    def build_player_repo(self) -> InMemoryPlayerRepository:
        """Build an InMemoryPlayerRepository"""
        result = InMemoryPlayerRepository()
        return result
