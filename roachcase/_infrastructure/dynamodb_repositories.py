import abc
import copy
import dataclasses
import boto3
import botocore
import collections
from typing import Dict, Any, Iterable, List
from roachcase import _entities, _repositories

import datetime


@dataclasses.dataclass
class Column:
    name: str
    ctype: str  # one of "S"
    is_primary: bool = False
    is_indexed: bool = False


class NoTableError(ValueError):
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


class DynamoDBGateway(DBGateway):
    """A wrapper around boto3 for dynamodb. Agnostic of the domain model
    Authentication must be set up correctly. See
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    """

    def __init__(self) -> None:
        self.__client = boto3.client("dynamodb")

    def __build_table_specs(
        self, table_name: str, columns: List[Column]
    ) -> Dict[str, Any]:

        keyschema = [
            {"AttributeName": column.name, "KeyType": "HASH"}
            for column in columns
            if column.is_primary
        ]
        attribute_definition = [
            {"AttributeName": column.name, "AttributeType": column.ctype}
            for column in columns
        ]
        result = {
            "TableName": table_name,
            "TableClass": "STANDARD",
            "KeySchema": keyschema,
            "AttributeDefinitions": attribute_definition,
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        }
        return result

    def list_tables(self) -> List[str]:
        """List names of tables"""
        response = self.__client.list_tables()
        result = [str(table) for table in response["TableNames"]]
        return result

    def remove_table(self, table_name: str) -> None:
        """Remove a table if it exists"""
        if table_name in self.list_tables():
            waiter = self.__client.get_waiter("table_not_exists")
            self.__client.delete_table(TableName=table_name)
            waiter.wait(TableName=table_name)

    def create_table(self, name: str, columns: List[Column]) -> None:
        """Create a table if it does not exist already"""
        template = copy.deepcopy(self.__build_table_specs(name, columns))
        template["TableName"] = name
        if name not in self.list_tables():
            response = self.__client.create_table(**template)
            waiter = self.__client.get_waiter("table_exists")
            waiter.wait(TableName=name)

    def add(self, table_name: str, item: Dict[str, Any]) -> None:
        """Add an item to a table"""
        try:
            self.__client.put_item(TableName=table_name, Item=item)
        except botocore.exceptions.ClientError as error:
            self.__handle_error(error)

    def get(self, table_name: str) -> Iterable[Dict[str, Any]]:
        """Get all items from a table"""
        try:
            response = self.__client.scan(TableName=table_name)
        except botocore.exceptions.ClientError as error:
            self.__handle_error(error)
        for item in response["Items"]:
            yield item

    def delete(self, table_name: str, item: Dict[str, Any]) -> None:
        """Delete an interm from a table"""
        try:
            self.__client.delete_item(Key=item, TableName=table_name)
        except botocore.exceptions.ClientError as error:
            self.__handle_error(error)

    def __handle_error(self, error: botocore.exceptions.ClientError) -> None:
        if error.response["Error"]["Code"] == "ResourceNotFoundException":
            raise NoTableError()
        else:
            raise error


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


class DBPlayerRepository(_repositories.PlayerRepository):
    """A conversion layers from the domain layer to the database persistence"""

    __columns = [Column(name="name", ctype="S", is_primary=True)]

    def __init__(self, db_gateway: DBGateway) -> None:
        self.__db_gateway = db_gateway
        self.__table_name = "players"

    def add(self, player: _entities.Player) -> None:

        current_players = self.get()
        if player in current_players:
            raise _repositories.PlayerAlreadyExistError()
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
