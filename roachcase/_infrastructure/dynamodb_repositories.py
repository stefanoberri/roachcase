import boto3
import botocore
import collections
from typing import Dict, Any, Iterable, List
from roachcase import _entities, _repositories

import datetime


class NoTableError(ValueError):
    pass


class DynamoDBGateway:
    """A wrapper around boto3 for dynamodb. Agnostic of the domain model
    Authentication must be set up correctly. See
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    """

    def __init__(self) -> None:
        self.__client = boto3.client("dynamodb")

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

    def create_table(self, specs: Dict[str, Any]) -> None:
        """Create a table if it does not exist already"""
        table_name = specs["TableName"]
        if table_name not in self.list_tables():
            response = self.__client.create_table(**specs)
            waiter = self.__client.get_waiter("table_exists")
            waiter.wait(TableName=table_name)

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


class DynamoDBPlayerGateway:
    """A conversion layers from the domain layer to the DynamoDB persistence"""

    def __init__(self, dynamodb: DynamoDBGateway) -> None:
        self.__dynamodb = dynamodb
        self.__specs = {
            "TableName": "players",
            "TableClass": "STANDARD",
            "KeySchema": [
                {"AttributeName": "name", "KeyType": "HASH"},
            ],
            "AttributeDefinitions": [
                {"AttributeName": "name", "AttributeType": "S"},
            ],
            "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        }

    def get_table_name(self) -> str:
        return str(self.__specs["TableName"])

    def set_table_name(self, name: str) -> None:
        self.__specs["TableName"] = name

    def get_table_specs(self) -> Dict[str, Any]:
        return self.__specs

    def convert_player_to_item(self, player: _entities.Player) -> Dict[str, Any]:
        result = {"name": {"S": player.get_name()}}
        return result

    def convert_item_to_player(self, item: Dict[str, Any]) -> _entities.Player:
        result = _entities.Player(item["name"]["S"])
        return result

    def add(self, player: _entities.Player) -> None:
        item = {"name": {"S": player.get_name()}}
        self.__dynamodb.add(self.get_table_name(), item)

    def get(self) -> Iterable[_entities.Player]:
        for item in self.__dynamodb.get(self.get_table_name()):
            result = _entities.Player(item["name"]["S"])
            yield result


class DynamoDBPlayerRepository(_repositories.PlayerRepository):
    """Repository to get and add Players to DynamoDB. It uses boto3 to interact
    with AWS."""

    def __init__(self, player_specs: DynamoDBPlayerGateway, gateway: DynamoDBGateway):
        self.__player_specs = player_specs
        self.__gateway = gateway

    def add(self, player: _entities.Player) -> None:
        """Add a player to the repository"""
        item = self.__player_specs.convert_player_to_item(player)
        self.__gateway.create_table(self.__player_specs.get_table_specs())
        current_players = self.get()
        if player in current_players:
            raise _repositories.PlayerAlreadyExistError()
        self.__gateway.add(self.__player_specs.get_table_name(), item)

    def get(self) -> Iterable[_entities.Player]:
        """Get players from the repository"""

        for item in self.__gateway.get(self.__player_specs.get_table_name()):
            player = self.__player_specs.convert_item_to_player(item)
            yield player
