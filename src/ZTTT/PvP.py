from .ZTBase import ZTBaseBoard


class PvP(ZTBaseBoard):

    def __init__(self):
        super().__init__()

    def play(self, pos: int):
        if self.turn == 1:
            super()._play_player_one_move(pos)
        else:
            super()._play_player_two_move(pos)
