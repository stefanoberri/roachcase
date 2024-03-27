import pytest

from roachcase._infrastructure import dynamodb_repositories
from roachcase import _entities
from tests import test_repositories
from tests.fixtures import john
import botocore


@pytest.fixture
def gateway():
    result = dynamodb_repositories.DynamoDBGateway()
    return result


class TestPlayerSpecs:
    @pytest.fixture
    def player_specs(self, gateway):
        result = dynamodb_repositories.DynamoDBPlayerGateway(gateway)
        result.set_table_name("__testing_players")
        return result

    def test_set_get_table_name(self, player_specs):
        player_specs.set_table_name("__another_testing_players")
        assert player_specs.get_table_name() == "__another_testing_players"

    def test_convert_player_to_item(self, player_specs):
        provided = _entities.Player("John")
        expected = {"name": {"S": "John"}}
        observed = player_specs.convert_player_to_item(provided)
        assert expected == observed

    def test_get_add_roundtrip(self, player_specs, john):
        player_specs.add(john)
        expected = [john]
        observed = player_specs.get()
        assert list(observed) == expected


class TestDynamoDBGateway:
    @pytest.mark.livedb
    def test_list_tables(self, gateway):
        observed = gateway.list_tables()
        # This interacts with the real database, we don't have expectations on
        # the tables available
        assert isinstance(observed, list)

    @pytest.mark.slow
    @pytest.mark.livedb
    def test_add_get_item_on_empty_table(self, gateway):
        specs = dynamodb_repositories.DynamoDBPlayerGateway()
        table_name = "__a_table_to_delete__"
        specs.set_table_name(table_name)
        gateway.remove_table(table_name)
        item = {"name": {"S": "Player1"}}
        # No table, we raise an error
        with pytest.raises(dynamodb_repositories.NoTableError):
            response = gateway.add(table_name, item)

        gateway.create_table(specs.get_table_specs())
        gateway.add(table_name, item)


class TestDynamoDBPlayerRepository(test_repositories.TestInMemoryPlayerRepository):
    """The same test for the in memory repository should also pass the
    DynamoDB repository."""

    @pytest.fixture
    def repo(self, gateway):
        player_specs = dynamodb_repositories.DynamoDBPlayerGateway()
        # we want to start from an empty table
        for item in gateway.get(player_specs.get_table_name()):
            gateway.delete(table_name=player_specs.get_table_name(), item=item)

        result = dynamodb_repositories.DynamoDBPlayerRepository(
            player_specs=player_specs, gateway=gateway
        )
        return result

    @pytest.mark.livedb
    def test_round_trip(self, john, repo):
        super().test_round_trip(john, repo)

    @pytest.mark.livedb
    def test_adding_player_with_same_name_raises(self, john, repo):
        super().test_adding_player_with_same_name_raises(john, repo)
