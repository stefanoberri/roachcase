import boto3
from typing import Iterable, List
from roachcase import _entities, _repositories

import datetime

player_dynamo_db_specs = {
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


class PlayerSpecs:
    def __init__(self, specs: dict):
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

    def get_table_name(self):
        return self.__specs["TableName"]


class DynamoDBGateway:
    """A wrapper around boto3 for dynamodb"""

    def __init__(self):
        self.__client = boto3.client("dynamodb")

    def list_tables(self) -> List[str]:
        response = self.__client.list_tables()
        result = response["TableNames"]
        return result

    def remove_table(self, table_name: str) -> None:
        if table_name in self.list_tables():
            waiter = self.__client.get_waiter("table_not_exists")
            self.__client.delete_table(TableName=table_name)
            waiter.wait(TableName=table_name)

    def create_table(self, specs: dict) -> None:
        table_name = specs["TableName"]
        if table_name not in self.list_tables():
            response = self.__client.create_table(**specs)
            waiter = self.__client.get_waiter("table_exists")
            waiter.wait(TableName=table_name)

    def add(self, table_name: str, item: dict) -> None:
        self.__client.put_item(TableName=table_name, Item=item)


class DynamoDBPlayerRepository(_repositories.PlayerRepository):
    """Repository to get and add Players to DynamoDB. It uses boto3 to interact
    with AWS.

    Authentication must be set up correctly. See
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    """

    def __init__(self, table_name: str, gateway: DynamoDBGateway):
        self.__gateway = gateway
        self.__table_name = table_name
        self.__client = boto3.client("dynamodb")
        self.__resource = boto3.resource("dynamodb")
        self.__table = self.__resource.Table(self.__table_name)

    def add(self, player: _entities.Player) -> None:
        """Add a player to the repository"""
        self.__create_table_if_not_exists()
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.__table_name)
        current_players = list(self.get())
        if player in current_players:
            raise _repositories.PlayerAlreadyExistError()
        else:
            item = {"name": player.get_name()}
            table.put_item(Item=item)

    def get(self) -> Iterable[_entities.Player]:
        """Get players from the repository"""
        result = []
        if self.__table_exist():
            response = self.__table.scan()
            items = response["Items"]
            for item in items:
                player = _entities.Player(item["name"])
                result.append(player)
        return result

    def delete_table_content(self) -> None:
        if self.__table_exist():
            dynamodb = boto3.resource("dynamodb")
            table = dynamodb.Table(self.__table_name)
            scan = table.scan()
            with table.batch_writer() as batch:
                for item in scan["Items"]:
                    batch.delete_item(Key={"name": item["name"]})

    def __create_table_if_not_exists(self) -> None:
        if not self.__table_exist():
            self.__create_table()

    def __table_exist(self) -> bool:
        response = self.__client.list_tables()
        result = self.__table_name in response["TableNames"]
        return result

    def __create_table(self) -> None:
        # Create the DynamoDB table.
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.create_table(
            TableName=self.__table_name,
            TableClass="STANDARD",
            KeySchema=[
                {"AttributeName": "name", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "name", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        # Wait until the table exists.
        table.wait_until_exists()
