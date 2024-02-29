==============
The roach case
==============

.. image:: img/roachcase.png
  :width: 400
  :alt: The roach case
  :align: center


A match making algorithm
------------------------

The *roach case* is a match making algorithm to create balanced teams from a set
of players with different skills. It has two purposes:

* Iteratively estimate player's skill level based on the outcome of played
  matches.

* Use the player's latest estimated skill level to create balanced teams.

Each player's skill level is measured in *roaches* stored in a *roach case*.
After each match, *roaches* are traded, depending on the outcome.

It is inspired by the `ELO scoring system`_ used in chess and other games.

A Python package
----------------

This Python package contains the *business logic* of the match making
algorithm, together with a very simple *command line interface* and simple
persistence layers. Other components can use it and extend it with a different
interface (web, standalone, ...) and more scalable persistence (local or cloud
database). Design is heavily inspired by `Clean Architecture`_ and/or `Onion
Architecture`_.


.. _Elo scoring system: https://en.wikipedia.org/wiki/Elo_rating_system
.. _Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
.. _Onion Architecture: https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
