import pytest
import roachcase


def test_set_persistence():
    observed = roachcase.list_players()
    assert observed == []
    roachcase.add_player("Bob")
    observed = roachcase.list_players()
    assert observed == ["Bob"]
    # this resets persistence
    roachcase.set_persistence("memory")
    observed = roachcase.list_players()
    assert observed == []


def test_add_list_players():
    roachcase.set_persistence("memory")
    observed = roachcase.list_players()
    assert observed == []
    roachcase.add_player("Bob")
    roachcase.add_player("Alice")
    observed = roachcase.list_players()
    assert set(observed) == set(["Alice", "Bob"])
    roachcase.set_persistence("memory")
    observed = roachcase.list_players()
    assert observed == []
