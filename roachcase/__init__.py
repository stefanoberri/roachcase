"""The API for the module. Only these functions/classes are exposed.

The API is a "controller" for the business logic
"""

import functools
from typing import List
from roachcase._usecases import factories


def list_players() -> List[str]:
    """List all players registered to the roachcase"""
    factory = _get_use_case_factory()
    use_case = factory.build_manage_players()
    result = list(use_case.list_players())
    return result


def add_player(player: str) -> None:
    """Register a player to the roachcase"""
    factory = _get_use_case_factory()
    use_case = factory.build_manage_players()
    use_case.add_player(player)


@functools.lru_cache()
def _get_use_case_factory() -> factories.UseCaseFactory:
    result = factories.UseCaseFactory()
    return result
