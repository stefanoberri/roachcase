import abc
import dataclasses
import functools
from typing import Any, Iterable, List, Dict
from roachcase import _entities


@dataclasses.dataclass
class Column:
    name: str
    ctype: str  # one of "S"
    is_primary: bool = False
    is_indexed: bool = False


class NoTableError(ValueError):
    pass


class PlayerAlreadyExistError(ValueError):
    pass


class DBGateway(abc.ABC):
    """Interface for a generic datatabase gateway where storage happens in
    'tables' with 'columns'. Agnostic of the domain model."""

    @abc.abstractmethod
    def list_tables(self) -> List[str]:
        """List names of available tables"""

    @abc.abstractmethod
    def remove_table(self, table_name: str) -> None:
        """Remove a table by name"""

    @abc.abstractmethod
    def create_table(self, name: str, columns: List[Column]) -> None:
        """Create a table by name and column specifications"""

    @abc.abstractmethod
    def add(self, table_name: str, item: Dict[str, Any]) -> None:
        """Add an item to `table_name`"""

    @abc.abstractmethod
    def get(self, table_name: str) -> Iterable[Dict[str, Any]]:
        """Get items from `table_name`"""

    @abc.abstractmethod
    def delete(self, table_name: str, item: Dict[str, Any]) -> None:
        """Delete an intem from a table"""


class InMemoryDBGateway(DBGateway):
    """An implementation of DBGateway which does not actually connect to
    real persistence, but stores entries in memories"""

    def __init__(self) -> None:
        self.__store: Dict[str, Any] = {}

    def list_tables(self) -> List[str]:
        return list(self.__store.keys())

    def remove_table(self, table_name: str) -> None:
        if table_name in self.__store:
            del self.__store[table_name]

    def create_table(self, name: str, columns: List[Column]) -> None:
        if name not in self.__store:
            self.__store[name] = []

    def add(self, table_name: str, item: Dict[str, Any]) -> None:
        """Add an item to a table"""
        self.__raise_if_no_table(table_name)
        if item not in self.__store[table_name]:
            self.__store[table_name].append(item)

    def get(self, table_name: str) -> Iterable[Dict[str, Any]]:
        """Get all items from a table"""
        self.__raise_if_no_table(table_name)
        for item in self.__store[table_name]:
            yield item

    def delete(self, table_name: str, item: Dict[str, Any]) -> None:
        """Delete an interm from a table"""
        self.__raise_if_no_table(table_name)
        self.__store[table_name].remove(item)

    def __raise_if_no_table(self, table_name: str) -> None:
        if table_name not in self.__store:
            raise NoTableError()


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


class DBPlayerRepository(PlayerRepository):
    """A conversion layers from the domain layer to the database persistence"""

    __columns = [Column(name="name", ctype="S", is_primary=True)]

    def __init__(self, db_gateway: DBGateway) -> None:
        self.__db_gateway = db_gateway
        self.__table_name = "players"

    def add(self, player: _entities.Player) -> None:

        current_players = self.get()
        if player in current_players:
            raise PlayerAlreadyExistError()
        else:
            item = {"name": {"S": player.get_name()}}
            try:
                self.__db_gateway.add(self.get_table_name(), item)
            except NoTableError:
                self.__db_gateway.create_table(self.__table_name, self.__columns)
                self.__db_gateway.add(self.get_table_name(), item)

    def get(self) -> Iterable[_entities.Player]:
        if self.get_table_name() in self.__db_gateway.list_tables():
            for item in self.__db_gateway.get(self.get_table_name()):
                result = _entities.Player(item["name"]["S"])
                yield result

    def get_table_name(self) -> str:
        return self.__table_name

    def set_table_name(self, name: str) -> None:
        self.__table_name = name


class InMemoryRepositoryFactory(RepositoryFactory):
    @functools.lru_cache()
    def build_player_repo(self) -> InMemoryPlayerRepository:
        """Build an InMemoryPlayerRepository"""
        result = InMemoryPlayerRepository()
        return result
