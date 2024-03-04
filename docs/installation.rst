.. highlight:: shell

============
Installation
============


Stable release
--------------

To install `roachcase`, run this command in your terminal:

.. code-block:: console

    $ pip install roachcase

This is the preferred method to install `roachcase`, as it will always
install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

You might also want to run the `pip install` command in a `virtual environment`_.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _virtual environment: https://docs.python-guide.org/dev/virtualenvs/#virtualenvwrapper


From sources
------------

The sources for `roachcase` can be downloaded from the `Github repo`_.

You can clone the public repository:

.. code-block:: console

    $ git clone git://github.com/stefanoberri/roachcase
    $ cd roachcase

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ make clean install IS_RELEASE=1

.. note::
    When installing from source, the version is not necessarily the same you
    would get when installing from pypi. The release versions (i.e. `X.Y.Z`)
    should not differ, but the beta versions (i.e. versions like `X.Y.ZbNM`)
    are currently not easy to reproduce.

.. _Github repo: https://github.com/stefanoberri/roachcase
