from ._zt_core import ZTEngineFirst
from ._zt_core import ZTPlayerFirst


class PvC(ZTEngineFirst, ZTPlayerFirst):
    """Class for the PvC Game"""

    def __init__(self, _engine_first: bool = True) -> None:
        """Initialize the Game

        :param _engine_first: Specifies if the engine starts first
        :type _engine_first: bool
        :return: None
        """

        if _engine_first:
            self.parent = ZTEngineFirst
            ZTEngineFirst.__init__(self)

        else:
            self.parent = ZTPlayerFirst
            ZTPlayerFirst.__init__(self)

    def play(self, pos: int) -> None:
        """Plays the player's move at the position specified

        :param pos: The position to play the player's move
        :type pos: int
        :return: None
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        self.parent.play(self, pos)
