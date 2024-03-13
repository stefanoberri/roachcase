.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

If you find a bug, please `file an issue`_

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to `file an issue`_

.. _file an issue: https://github.com/stefanoberri/roachcase/issues

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Add external functionality
~~~~~~~~~~~~~~~~~~~~~~~~~~

This codebase is written to be modular and trying to adhere to the `open-closed
principle`_, so it should be possible to extend its behaviour (e.g. adding a
different persistence layer) without heavily modifying this codebase.

.. _open-closed principle: https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle

Development
-----------

Ready to contribute? Here's how to set up `roachcase` for local development.

* Fork the `roachcase` repo on GitHub.
* Clone your fork locally::

    $ git clone git@github.com:your_name_here/roachcase.git

* You can optionally set up a `virtual environment`_ first, then install
  development prerequisites::

    $ python -m pip install -r requirements_dev.txt

* You can now run tests locally. Before you make any change you should make
  sure these commands complete successfully::

    $ make test
    $ make typecheck
    $ make lint
    $ make docs_templates

* Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

* Now you can make your changes locally. As you make changes and before
  committing, please re-run the commands above to show that all tests are still
  passing.

* Commit your changes and push your branch to GitHub. Please write a `useful
  commit message`_::

    $ git add -u
    $ git commit
    $ git push origin name-of-your-bugfix-or-feature

* Submit a pull request through the GitHub website.

.. _virtual environment: https://docs.python-guide.org/dev/virtualenvs/#virtualenvwrapper
.. _useful commit message: https://cbea.ms/git-commit/

Tips
----

To run a subset of tests, with verbose output and exit at first failure::

$ python3 -m pytest -vvvv -x tests/test_entities.py
