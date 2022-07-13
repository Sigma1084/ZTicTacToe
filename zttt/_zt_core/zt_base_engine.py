from typing import Tuple, List
from random import choice

from .zt_base_board import ZTBaseBoard
from ..zt_errors import *


class ZTBaseEngine(ZTBaseBoard):
    """Base Class for the Engine"""

    def __init__(self, _engine_first: bool) -> None:
        """Initialize the State Variables in an Engine

        :param _engine_first: Specifies if the engine starts first
        :type _engine_first: bool
        :return: None
        """

        super().__init__()

        # Private since we don't want people to change it
        self.__engine_first: bool = _engine_first

        # List of all the lines that contain at least one empty position
        self.__active_lines: List[Tuple[int, int, int]] = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

    # Properties

    @property
    def engine_first(self) -> bool:
        """Returns if the engine starts first

        :return: True if the engine starts first, False otherwise
        :rtype: bool
        """
        return self.__engine_first

    @property
    def _engine_value(self) -> int:
        """Returns the value of the engine and is mainly for development purpose

        :return: The value of the engine
        :rtype: int
        """
        return self.__class__._VAL_PLAYER1 if self.__engine_first is True else self.__class__._VAL_PLAYER2

    @property
    def _player_value(self) -> int:
        """Returns the value of the player and is mainly for development purpose

        :return: The value of the engine
        :rtype: int
        """
        return self.__class__._VAL_PLAYER1 if self.__engine_first is False else self.__class__._VAL_PLAYER2

    # Bot Functions

    def _calc_line_weight(self, _line: Tuple[int, int, int], _board_list: List[int] = None) -> int:
        """Calculates the weight of a line

        :param _line: The line to calculate the weight of
        :type _line: Tuple[int, int, int]
        :param _board_list: If specified, the board list to use instead of the current one
        :type _board_list: List[int]
        :return: The weight of the line (Sum of the values of the positions)
        :rtype: int
        :raises ZTBadFunctionCall: If the board list is not in proper format
        """

        if _board_list is None:
            _board_list = self._board_list
        elif len(_board_list) != 9:
            raise ZTBadFunctionCall("The Board List length must be 9")
        else:
            for pos_val in _board_list:
                if pos_val not in (self._VAL_PLAYER1, self._VAL_PLAYER2, self._VAL_EMPTY):
                    raise ZTBadFunctionCall(f"Board List not in the correct format, {pos_val} invalid")

        # The verification is complete
        return sum([_board_list[pos] for pos in _line])

    def _get_winnable_moves(self) -> List[int]:
        """Returns a list of winnable moves and empty list if none

        :return: A list of winnable moves
        :rtype: List[int]
        """

        winnable_moves = []
        for line in self.__active_lines:
            line_weight = self._calc_line_weight(line)
            if line_weight == 2 * self._engine_value:
                if self._board_list[line[0]] == self._VAL_EMPTY:
                    winnable_moves.append(line[0])
                elif self._board_list[line[1]] == self._VAL_EMPTY:
                    winnable_moves.append(line[1])
                else:
                    winnable_moves.append(line[2])

        return winnable_moves

    def _get_danger_move(self) -> List[int]:
        """Returns the move to avoid losing, else nothing

        :return: The singleton list with the only move to avoid losing, empty list otherwise
        :rtype: List[int]
        """

        for line in self.__active_lines:
            line_weight = self._calc_line_weight(line)
            if line_weight == 2 * self._player_value:
                if self._board_list[line[0]] == self._VAL_EMPTY:
                    return [line[0]]
                elif self._board_list[line[1]] == self._VAL_EMPTY:
                    return [line[1]]
                else:
                    return [line[2]]
        return []

    def __get_double_danger_moves(self) -> List[int]:
        """Returns a list of moves that cause double attacks, empty list if none

        :return: List of moves that cause double danger
        :rtype: List[int]
        """

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

    def _get_bot_move(self) -> List[int]:
        """Returns the best move to play using the above functions

        :return: The singleton list with the only move to play, empty list otherwise
        :rtype: List[int]
        """

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

    def __clean(self, pos: int) -> None:
        """Clean the active lines list maintained by the engine

        :param pos: The last position played
        :type pos: int
        :return: None
        """

        if self.move < 5:
            return
        for (pos1, pos2) in self._LINES[pos]:
            if sorted([pos, pos1, pos2]) in self.__active_lines and self._board_list[pos1] != self._VAL_EMPTY \
                    and self._board_list[pos2] != self._VAL_EMPTY:
                self.__active_lines.remove(sorted([pos, pos1, pos2]))

    # Functions to play

    def _play_engine(self, pos: int) -> None:
        """Play the engine move. Also cleans the active lines list

        :param pos: Position for engine to play
        :type pos: int
        :return: None
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        if self.__engine_first:
            self._play_player_one_move(pos)
        else:
            self._play_player_two_move(pos)
        pos = int(pos)
        self.__clean(pos)

    def _play_player(self, pos: int) -> None:
        """Play the player move. Also cleans the active lines list

        :param pos: Position for player to play
        :type pos: int
        :return: None
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        if not self.__engine_first:
            self._play_player_one_move(pos)
        else:
            self._play_player_two_move(pos)
        pos = int(pos)
        self.__clean(pos)
