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


@pytest.fixture
def player_repo(gateway):
    result = dynamodb_repositories.DynamoDBPlayerRepository(gateway)
    result.set_table_name("__testing_players")
    return result


@pytest.fixture
def empty_player_repository(gateway):
    # we want to start from an empty table
    table_name = "__testing_players"
    for item in gateway.get(table_name):
        gateway.delete(table_name=table_name, item=item)
    result = dynamodb_repositories.DynamoDBPlayerRepository(gateway)
    result.set_table_name(table_name)
    return result


class TestDynamoDBGateway:
    @pytest.mark.livedb
    def test_list_tables(self, gateway):
        observed = gateway.list_tables()
        # We don't have expectations on # the tables available
        assert isinstance(observed, list)

    @pytest.mark.slow
    @pytest.mark.livedb
    def test_add_get_item_on_empty_table(self, gateway, player_repo):
        table_name = "__a_table_to_delete__"
        player_repo.set_table_name(table_name)
        gateway.remove_table(table_name)
        item = {"name": {"S": "Player1"}}
        # No table, we raise an error
        with pytest.raises(dynamodb_repositories.NoTableError):
            response = gateway.add(table_name, item)

        columns = [dynamodb_repositories.Column(name="name", ctype="S", is_primary=True)]
        gateway.create_table(table_name, columns=columns)

        # gateway.create_table(player_repo.get_table_specs())
        # no error raised now
        gateway.add(table_name, item)
        assert table_name in gateway.list_tables()
        observed = gateway.get(table_name)
        assert list(observed) == [item]


class TestInMemoryDBGateway(TestDynamoDBGateway):
    @pytest.fixture
    def gateway(self):
        result = dynamodb_repositories.InMemoryDBGateway()
        return result

    def test_list_tables(self, gateway):
        super().test_list_tables(gateway)

    def test_add_get_item_on_empty_table(self, gateway, player_repo):
        super().test_add_get_item_on_empty_table(gateway, player_repo)


class TestDynamoDBPlayerRepository(test_repositories.TestInMemoryPlayerRepository):

    def test_set_get_table_name(self, player_repo):
        player_repo.set_table_name("__another_testing_players")
        assert player_repo.get_table_name() == "__another_testing_players"

    def test_get_add_roundtrip(self, empty_player_repository, john):
        empty_player_repository.add(john)
        expected = [john]
        observed = empty_player_repository.get()
        assert list(observed) == expected

    @pytest.mark.livedb
    def test_round_trip(self, john, empty_player_repository):
        super().test_round_trip(john, empty_player_repository)

    @pytest.mark.livedb
    def test_adding_player_with_same_name_raises(self, john, empty_player_repository):
        super().test_adding_player_with_same_name_raises(john, empty_player_repository)
