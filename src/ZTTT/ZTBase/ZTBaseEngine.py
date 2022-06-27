from typing import Tuple, List
from random import choice

# from ZTTT.ZTBase.ZTBaseBoard import ZTBaseBoard
# from ..ZTBase.ZTBaseBoard import ZTBaseBoard
# from ..ZTBase.ZTErrors import *
from src.ZTTT.ZTBase import *


class ZTBaseEngine(ZTBaseBoard):

    def __init__(self, _engine_first: bool):
        super().__init__()

        # Private since we don't want people to change it
        self.__engine_first: bool = _engine_first

        # List of all the lines that contain at least one empty position
        self.__active_lines: List[Tuple[int, int, int]] = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

    @property
    def engine_first(self) -> bool:
        return self.__engine_first

    @property
    def _engine_value(self) -> int:
        return ZTBaseBoard._VAL_PLAYER1 if self.__engine_first is True else ZTBaseBoard._VAL_PLAYER2

    @property
    def _player_value(self) -> int:
        return ZTBaseBoard._VAL_PLAYER1 if self.__engine_first is False else ZTBaseBoard._VAL_PLAYER2

    def _calc_line_weight(self, _line: Tuple[int, int, int], _board_list: List[int] = None) -> int:
        if _board_list is None:
            _board_list = self._board_list
        elif len(_board_list) != 9:
            raise ZTBadFunctionCall("The Board List length must be 9")
        else:
            for pos_val in _board_list:
                if pos_val not in (ZTBaseBoard._VAL_PLAYER1, ZTBaseBoard._VAL_PLAYER2, ZTBaseBoard._VAL_EMPTY):
                    raise ZTBadFunctionCall(f"Board List not in the correct format, {pos_val} invalid")

        # The verification is complete
        return sum([_board_list[pos] for pos in _line])

    # Returns a list of winnable moves and empty list if none
    def _get_winnable_moves(self) -> List[int]:
        winnable_moves = []
        for line in self.__active_lines:
            line_weight = self._calc_line_weight(line)
            if line_weight == 2 * self._engine_value:
                if self._board_list[line[0]] == ZTBaseBoard._VAL_EMPTY:
                    winnable_moves.append(line[0])
                elif self._board_list[line[1]] == ZTBaseBoard._VAL_EMPTY:
                    winnable_moves.append(line[1])
                else:
                    winnable_moves.append(line[2])

        return winnable_moves

    # Returns the only move to avoid losing else False
    def _get_danger_move(self) -> List[int]:
        for line in self.__active_lines:
            line_weight = self._calc_line_weight(line)
            if line_weight == 2 * self._player_value:
                if self._board_list[line[0]] == ZTBaseBoard._VAL_EMPTY:
                    return [line[0]]
                elif self._board_list[line[1]] == ZTBaseBoard._VAL_EMPTY:
                    return [line[1]]
                else:
                    return [line[2]]
        return []

    # Returns a list of moves that cause double danger and empty list if none
    def __get_double_danger_moves(self) -> List[int]:
        double_danger_moves = []
        for corner in self.empty_corners:
            count = 0
            new_board_list = self.board_list
            new_board_list[corner] = self._engine_value
            for line in self.__active_lines:
                line_weight = self._calc_line_weight(line, new_board_list)
                if line_weight == 2 * self._engine_value:
                    count += 1
                if count == 2:
                    break
            if count == 2:
                double_danger_moves.append(corner)
        return double_danger_moves

    # This function uses the above functions and decides on a move
    def _get_bot_move(self) -> List[int]:
        temp = self._get_winnable_moves()
        if temp:
            return [choice(temp)]

        temp = self._get_danger_move()
        if temp:
            return [choice(temp)]

        temp = self.__get_double_danger_moves()
        if temp:
            return [choice(temp)]

        return []

    # Defining _play_engine and _play_player to make the code more understandable
    def __clean(self, pos: int) -> None:
        # Clean and update the self.__active_lines
        if self.move < 5:
            return
        for (pos1, pos2) in ZTBaseBoard.LINES[pos]:
            if sorted([pos, pos1, pos2]) in self.__active_lines and self._board_list[pos1] != ZTBaseBoard._VAL_EMPTY \
                    and self._board_list[pos2] != ZTBaseBoard._VAL_EMPTY:
                self.__active_lines.remove(sorted([pos, pos1, pos2]))

    def _play_engine(self, pos: int) -> None:
        self.__clean(pos)
        if self.__engine_first:
            self._play_player_one_move(pos)
        else:
            self._play_player_two_move(pos)

    def _play_player(self, pos: int) -> None:
        self.__clean(pos)
        if not self.__engine_first:
            self._play_player_one_move(pos)
        else:
            self._play_player_two_move(pos)
