========
Tutorial
========

The `roach case` is a `case` where players keep their valuable `roaches` and exchange them
when playing a match, depending on the outcome.

Here an example on how to use the Python API. Import the package::

    import roachcase

By default there is no persistance, data is stored in memory, but you can
specify persistance to store data across sessions. Currently only file
persistance is supported::

    roachcase.set_persistence("shelf", path="/path/to/a/file")

Regardless of persistence, we can now register players to the `roach case`::

    roachcase.add_player("Alice")
    roachcase.add_player("Bob")

We can now retrieve all the registered players::

    roachcase.list_players()

And we should get the following::

    ['Alice', 'Bob']
