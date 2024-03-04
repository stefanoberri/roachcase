import roachcase


def test_add_list_players():
    observed = roachcase.list_players()
    assert observed == []
    roachcase.add_player("Bob")
    roachcase.add_player("Alice")
    observed = roachcase.list_players()
    assert set(observed) == set(["Alice", "Bob"])
