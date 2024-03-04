========
Tutorial
========

The `roachcase` is a place where players keep their `roaches` and exchange them
when playing a match, depending on the outcome.

To start, we need to register players to the `roachcase`::

    import roachcase

    # currently there is no persistance, data is stored in memory

    roachcase.add_player("Alice")
    roachcase.add_player("Bob")

We can now retrieve all the registered players::

    roachcase.list_players()

And we should get the following::

    ['Alice', 'Bob']
