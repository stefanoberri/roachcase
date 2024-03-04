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
def in_memory_repository():
    result = _repositories.InMemoryPlayerRepository()
    return result
