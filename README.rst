
==============
The roach case
==============

.. image:: https://readthedocs.org/projects/roachcase/badge
        :target: https://roachcase.readthedocs.io/en/latest
        :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/roachcase.svg
        :target: https://pypi.python.org/pypi/roachcase

.. image:: https://github.com/stefanoberri/roachcase/actions/workflows/test-package.yml/badge.svg
        :target: https://github.com/stefanoberri/roachcase/actions/workflows/test-package.yml


.. image:: https://roachcase.readthedocs.io/en/latest/_images/roachcase.png
  :width: 400
  :alt: The roach case
  :align: center


A match making algorithm
------------------------

The roach case is a match making algorithm to create balanced teams from players
with different skills. It has two purposes:

* Iteratively score player's skill level based on the outcome of played
  matches.

* Use the player's latest scores to create balanced teams.


Scores are converted into *roaches* each players has in the *roach case*. *Roaches*
are traded after each match, depending on the outcome.

It is inspired by the `ELO scoring system`_ used in chess and other games.

A Python package
----------------

This Python package contains the *business logic* of the match making
algorithm, available through its API. It also has a simple persistence layers.
Other components can use it and extend it with a different interface (web,
standalone, ...) and more scalable persistence (local or cloud database).
Design is heavily inspired by `Clean Architecture`_ and/or `Onion
Architecture`_.

Documentation
-------------

Please read the latest `documentation`_ online

Credits
-------

Stefano Berri

.. _Elo scoring system: https://en.wikipedia.org/wiki/Elo_rating_system
.. _Clean Architecture: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
.. _Onion Architecture: https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
.. _documentation: https://roachcase.readthedocs.io/en/latest/
