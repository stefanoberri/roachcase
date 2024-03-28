import pytest

from roachcase._infrastructure import dynamodb_repositories
from roachcase import _entities
from tests import test_repositories
from tests.fixtures import john
import botocore


@pytest.fixture
def in_memory_gateway():
    result = dynamodb_repositories.InMemoryDBGateway()
    return result


@pytest.fixture
def dynamodb_gateway():
    result = dynamodb_repositories.DynamoDBGateway()
    return result


class TestInMemoryDBGateway:
    @pytest.fixture
    def gateway(self, in_memory_gateway):
        return in_memory_gateway

    def test_list_tables(self, gateway):
        observed = gateway.list_tables()
        # We don't have expectations on # the tables available
        assert isinstance(observed, list)

    def test_add_get_item_on_empty_table(self, gateway):
        table_name = "__a_table_to_delete__"
        gateway.remove_table(table_name)
        item = {"name": {"S": "Player1"}}
        # No table, we raise an error
        with pytest.raises(dynamodb_repositories.NoTableError):
            response = gateway.add(table_name, item)

        columns = [
            dynamodb_repositories.Column(name="name", ctype="S", is_primary=True)
        ]
        gateway.create_table(table_name, columns=columns)

        # no error raised now
        gateway.add(table_name, item)
        assert table_name in gateway.list_tables()
        observed = gateway.get(table_name)
        assert list(observed) == [item]
        gateway.delete(table_name, item)
        observed = gateway.get(table_name)
        assert list(observed) == []

        # cleanup
        gateway.remove_table(table_name)



class TestDynamoDBGateway(TestInMemoryDBGateway):
    @pytest.fixture
    def gateway(self, dynamodb_gateway):
        return dynamodb_gateway

    @pytest.mark.livedb
    def test_list_tables(self, gateway):
        super().test_list_tables(gateway)

    @pytest.mark.slow
    @pytest.mark.livedb
    def test_add_get_item_on_empty_table(self, gateway):
        super().test_add_get_item_on_empty_table(gateway)


class TestDynamoDBPlayerRepository(test_repositories.TestInMemoryPlayerRepository):
    @pytest.fixture
    def player_repo(self, in_memory_gateway):
        result = dynamodb_repositories.DBPlayerRepository(in_memory_gateway)
        table_name = "__testing_players"
        result.set_table_name(table_name)
        return result

    def test_set_get_table_name(self, player_repo):
        player_repo.set_table_name("__another_testing_players")
        assert player_repo.get_table_name() == "__another_testing_players"

    def test_get_add_roundtrip(self, player_repo, john):
        player_repo.add(john)
        expected = [john]
        observed = player_repo.get()
        assert list(observed) == expected

    @pytest.mark.livedb
    def test_round_trip(self, john, player_repo):
        super().test_round_trip(john, player_repo)

    @pytest.mark.livedb
    def test_adding_player_with_same_name_raises(self, john, player_repo):
        super().test_adding_player_with_same_name_raises(john, player_repo)
