"""The API for roachcase"""

from typing import List, Union, Optional
import pathlib
from roachcase import _controller


def list_players() -> List[str]:
    """List all players registered to the roachcase"""
    return _controller.list_players()


def add_player(player: str) -> None:
    """Register a player to the roachcase"""
    _controller.add_player(player)


def set_persistence(
    persistence: str = "memory", path: Optional[Union[str, pathlib.Path]] = None
) -> None:
    """Set/Reset where data should persist.

    :param [persistence]: how to store the data. Available options are:
        "memory", "shelf".
    :param [path]: Optional path to the file for persistence. Will be created
        if does not exist

    With persistence = "memory", data will be lost at the end of a session.
    With persistence = "shelf", path must be set, and data will be persisted as
    a shelf/pickle database
    """
    _controller.set_persistence(persistence, path)
