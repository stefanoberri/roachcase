import pytest
import botocore

from roachcase._infrastructure import dynamodb_repositories
from tests import test_repositories


class TestDynamoDBGateway(test_repositories.TestInMemoryDBGateway):
    """Apply the same test for the InMemoryDBGateway to the DynamoDB one"""

    @pytest.fixture
    def gateway(self):
        result = dynamodb_repositories.DynamoDBGateway()
        return result

    @pytest.mark.livedb
    def test_list_tables(self, gateway):
        super().test_list_tables(gateway)

    @pytest.mark.slow
    @pytest.mark.livedb
    def test_add_get_item_on_empty_table(self, gateway):
        super().test_add_get_item_on_empty_table(gateway)
