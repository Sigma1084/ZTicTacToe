from typing import Dict, List
from random import choice

from ..ZTBase import ZTBaseEngine


class ZTEngineFirst(ZTBaseEngine):
    __ENGINE_MOVE: Dict[int, Dict[int, List[int]]] = {
        0: {1: [6, 4], 2: [6, 8], 3: [2, 4], 4: [5, 7], 5: [2, 4, 6], 6: [2, 8], 7: [2, 4, 6], 8: [2, 6]},
        2: {0: [6, 8], 1: [8, 4], 3: [0, 4, 8], 4: [3, 7], 5: [0, 4], 6: [0, 8], 7: [0, 4, 8], 8: [0, 6]},
        6: {0: [2, 8], 1: [0, 4, 8], 2: [0, 8], 3: [8, 4], 4: [1, 5], 5: [0, 4, 8], 7: [0, 4], 8: [0, 2]},
        8: {0: [2, 6], 1: [2, 4, 6], 2: [0, 6], 3: [2, 4, 6], 4: [1, 3], 5: [6, 4], 6: [0, 2], 7: [2, 4]}
    }

    def __init__(self):
        ZTBaseEngine.__init__(self, True)
        self.move1: int = choice([0, 2, 6, 8])
        self._play_engine(self.move1)

    # A function which is called in the main method if play is True
    def play(self, pos: int) -> None:
        self._play_player(pos)

        if self.move == 3:
            return self._play_engine(choice(ZTEngineFirst.__ENGINE_MOVE[self.move1][pos]))

        move = self._get_bot_move()
        if move:
            return self._play_engine(move[0])

        if self.empty_corners:
            return self._play_engine(choice(self.empty_corners))

        else:
            return self._play_engine(choice(self._empty_positions))
