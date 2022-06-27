from typing import Dict, Tuple, List

from ..ZTBase import ZTBaseEngine
from random import choice


class ZTPlayerFirst (ZTBaseEngine):
    __ENGINE_MOVE: Dict[Tuple[int, int], List[int]] = {
        (0, 8): [1, 3, 5, 7], (2, 6): [1, 3, 5, 7],  # Opposite corner cases
        (1, 7): [0, 2, 6, 8], (3, 5): [0, 2, 6, 8],  # Opposite edge cases
        (1, 3): [0], (1, 5): [2], (7, 3): [6], (7, 5): [8],  # Non-opposite edge cases
    }

    def __init__(self):
        ZTBaseEngine.__init__(self, False)
        self.center: bool = False  # This variable is True when the opponent plays center in move 1
        self.liberty_move3: bool = False  # This means choice of the third move is corners

    def __get_non_center_move2(self):
        for (pos1, pos2) in ZTPlayerFirst.__ENGINE_MOVE:
            if self._board_list[pos1] == self._player_value and self._board_list[pos2] == self._player_value:
                return choice(ZTPlayerFirst.__ENGINE_MOVE[(pos1, pos2)])

        non_center_lines: List[Tuple[int, int, int]] = [(0, 1, 2), (2, 5, 8), (6, 7, 8), (0, 3, 6)]
        for line in non_center_lines:
            line_weight = self._calc_line_weight(line)
            if line_weight == 2 * self._player_value:
                # One of the corner is empty implies a continuous draw game to the last move
                if self._board_list[line[0]] == self._VAL_EMPTY:
                    return line[0]
                if self._board_list[line[2]] == self._VAL_EMPTY:
                    return line[2]

                # The edge is empty introduces a liberty move in move 3
                self.liberty_move3 = True
                return line[1]

        # The remaining possibility is that the player has played in one corner and one edge
        # We just play opposite of the corner the player has played in

        # The remaining cases
        if self._board_list[0] == self._player_value:
            return 8
        if self._board_list[2] == self._player_value:
            return 6
        if self._board_list[6] == self._player_value:
            return 2
        if self._board_list[8] == self._player_value:
            return 0

    def play(self, inp: int):
        self._play_player(inp)

        if not self.status:
            return

        if self.move == 2:
            if inp == 4:
                self.center = True  # The player played the center so the best move is a corner
                return self._play_engine(choice(self.empty_corners))
            return self._play_engine(4)  # If the player does not start with center, the engine will

        if self.move == 4 and not self.center:
            return self._play_engine(self.__get_non_center_move2())

        if self.move == 4 and self.center:
            move = self._get_danger_move()
            if move:
                return self._play_engine(move[0])
            return self._play_engine(choice(self.empty_corners))

        # Special Cases Over
        move = self._get_bot_move()
        if move:
            return self._play_engine(move[0])

        if self.move == 6:
            if self.liberty_move3:
                return self._play_engine(choice(self.empty_edges))
            else:
                return self._play_engine(choice(self.empty_corners))

        if self.move == 8:
            return self._play_engine(choice(self._empty_positions))
