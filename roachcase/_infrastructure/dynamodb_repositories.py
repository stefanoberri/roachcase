import copy
import boto3
import botocore
from typing import Dict, Any, Iterable, List
from roachcase import _repositories


class DynamoDBGateway(_repositories.DBGateway):
    """A wrapper around boto3 for dynamodb. Agnostic of the domain model
    Authentication must be set up correctly. See
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    """

    def __init__(self) -> None:
        self.__client = boto3.client("dynamodb")

    def __build_table_specs(
        self, table_name: str, columns: List[_repositories.Column]
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

    def create_table(self, name: str, columns: List[_repositories.Column]) -> None:
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
            raise _repositories.NoTableError()
        else:
            raise error
