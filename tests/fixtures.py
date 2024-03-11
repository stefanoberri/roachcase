"""Shared fixtures. Similar to what conftest.py would do, but this is explicit
and only loads on request"""

import pytest
from roachcase import _entities, _repositories


@pytest.fixture
def john():
    """A player"""
    result = _entities.Player("John")
    return result


@pytest.fixture
def jane():
    """A player"""
    result = _entities.Player("Jane")
    return result


@pytest.fixture
def football():
    """A game"""
    result = _entities.Game(name="Football")
    return result


@pytest.fixture
def volleyball():
    """A game"""
    result = _entities.Game(name="Volleyball")
    return result


@pytest.fixture
def in_memory_repository_factory():
    result = _repositories.InMemoryRepositoryFactory()
    return result
