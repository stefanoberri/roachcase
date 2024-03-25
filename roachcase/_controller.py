"""Controller functionality"""

import functools
from typing import List, Optional, Union
import pathlib

from roachcase._usecases import factories
from roachcase import _repositories
from roachcase._infrastructure import shelf_repositories


def list_players() -> List[str]:
    """List all players registered to the roachcase"""
    factory = get_use_case_factory()
    use_case = factory.build_manage_players()
    result = list(use_case.list_players())
    return result


def add_player(player: str) -> None:
    """Register a player to the roachcase"""
    factory = get_use_case_factory()
    use_case = factory.build_manage_players()
    use_case.add_player(player)


def set_persistence(
    persistence: str = "memory", path: Optional[Union[str, pathlib.Path]] = None
) -> None:
    """Set/Reset where data should persist.

    :param [persistence]: how to store the data. Available options are:
        "memory", "shelf".
    :param [path]: Optional path to the file for persistence. Will be created
        if does not exist

    Details:
        with :param [persistence] = "memory", data will be lost at the end of a session
        with :param [persistence] = "shelf", path must be set, and data will be
            persisted as a shelf/pickle database
    """
    factory = get_use_case_factory()
    repo_factory: _repositories.RepositoryFactory
    if persistence == "memory":
        repo_factory = _repositories.InMemoryRepositoryFactory()
    elif persistence == "shelf":
        if path is None:
            raise ValueError("For persistence on `shelf`, `path` must be set")
        else:
            repo_factory = shelf_repositories.ShelfRepositoryFactory(pathlib.Path(path))
    else:
        raise ValueError
    factory.set_repo_factory(repo_factory)


def get_default_use_case_factory() -> factories.UseCaseFactory:
    """Build default use case factory"""
    repo_factory = _repositories.InMemoryRepositoryFactory()
    result = factories.UseCaseFactory(repo_factory)
    return result


@functools.lru_cache()
def get_use_case_factory() -> factories.UseCaseFactory:
    """Singleton to get the use case factory"""
    return get_default_use_case_factory()
