import pytest

from roachcase._infrastructure import dynamodb_repositories
from tests import test_repositories
from tests.fixtures import john


@pytest.fixture
def gateway():
    result = dynamodb_repositories.DynamoDBGateway()
    return result


class TestDynamoDBGateway:
    @pytest.mark.livedb
    def test_list_tables(self, gateway):
        observed = gateway.list_tables()
        # This interacts with the real database, we don't have expectations on
        # the tables available
        assert isinstance(observed, list)

    @pytest.mark.slow
    @pytest.mark.livedb
    def test_create_and_remove_table(self, gateway):
        specs = dynamodb_repositories.player_dynamo_db_specs
        provided = "__a_table_to_delete__"
        specs["TableName"] = provided
        # gateway.specs = specs
        gateway.remove_table(provided)
        assert provided not in gateway.list_tables()
        gateway.create_table(specs)
        assert provided in gateway.list_tables()
        gateway.remove_table(provided)
        assert provided not in gateway.list_tables()

    @pytest.mark.livedb
    def test_add_get_item(self, gateway):
        specs = dynamodb_repositories.player_dynamo_db_specs
        table_name = "__testing"
        specs["TableName"] = table_name
        gateway.create_table(specs)
        item = {"name": {"S": "Player1"}}
        gateway.add(table_name, item)



class TestDynamoDBPlayerRepository(test_repositories.TestInMemoryPlayerRepository):
    """The same test for the in memory repository should also pass the
    DynamoDB repository."""

    @pytest.fixture
    def repo(self, gateway):
        result = dynamodb_repositories.DynamoDBPlayerRepository(
            table_name="__testing_players", gateway=gateway
        )
        # we want to start from an empty repository
        result.delete_table_content()
        return result

    @pytest.mark.livedb
    def test_round_trip(self, john, repo):
        super().test_round_trip(john, repo)

    @pytest.mark.livedb
    def test_adding_player_with_same_name_raises(self, john, repo):
        super().test_adding_player_with_same_name_raises(john, repo)
