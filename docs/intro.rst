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

.. _Elo scoring system: https://en.wikipedia.org/wiki/Elo_rating_system
