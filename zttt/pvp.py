from ._zt_core import ZTBaseBoard


class PvP(ZTBaseBoard):

    def __init__(self) -> None:
        """Initialize the Game"""
        super().__init__()

    def play(self, pos: int) -> None:
        """Plays the player's move at the position specified

        :param pos: The position to play the player's move
        :type pos: int
        :return: None
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        if self.turn == 1:
            super()._play_player_one_move(pos)
        else:
            super()._play_player_two_move(pos)
