class Player:
    """Represents a Player"""

    def __init__(self, name: str):
        self.__name = name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.get_name() == other.get_name()
        else:
            return False

    def get_name(self) -> str:
        """Gets the name of the player"""
        return self.__name
