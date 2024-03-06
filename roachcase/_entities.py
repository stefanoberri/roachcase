class Player:
    """Represents a Player"""

    def __init__(self, name: str):
        self.__name = name

    def get_name(self) -> str:
        """Gets the name of the player"""
        return self.__name
