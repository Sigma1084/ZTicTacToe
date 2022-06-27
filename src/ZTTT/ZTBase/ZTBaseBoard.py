from typing import List, Tuple, Dict
from ..ZTErrors import *


# This is the main class which is inherited by all the classes which are used in the module
class ZTBaseBoard:
    _VAL_PLAYER1 = 4
    _VAL_PLAYER2 = 1
    _VAL_EMPTY = 0

    # Indicates what the values contained in the _board_list represent
    # The indicator with value 5 goes first
    _INDICATOR: Dict[int, str] = {
        _VAL_PLAYER1: 'X',
        _VAL_PLAYER2: 'O',
        _VAL_EMPTY: ' '
    }

    # All the lines the current position is a part of
    LINES: Dict[int, List[Tuple[int, int]]] = {
        4: [(0, 8), (2, 6), (1, 7), (3, 5)],

        0: [(1, 2), (4, 8), (3, 6)],
        2: [(1, 0), (4, 6), (5, 8)],
        6: [(3, 0), (4, 2), (7, 8)],
        8: [(5, 2), (4, 0), (6, 7)],

        1: [(0, 2), (4, 7)],
        3: [(0, 6), (4, 5)],
        5: [(2, 8), (3, 4)],
        7: [(6, 8), (4, 1)]
    }

    # The center is present in Position 4
    _CENTER = 4

    @classmethod
    def set_indicators(cls, _player1: str = 'X', _player2: str = 'O', _space: str = ' '):
        cls._INDICATOR = {
            cls._VAL_PLAYER1: str(_player1),
            cls._VAL_PLAYER2: str(_player2),
            cls._VAL_EMPTY: str(_space)
        }

    def __init__(self):

        # Main list containing the _empty_positions from top left in row major order
        # Protected since inherited classes will be able to quickly access it
        self._board_list: List[int] = [0 for _ in range(9)]

        # List containing the _empty_positions empty edges and empty corners
        # Protected since inherited classes will be able to quickly access it
        self._empty_positions: List[int] = [i for i in range(9)]

        # History
        self._history: List[int] = []

        # Determines whether the game is ongoing or not
        self.__status: bool = True

        # Stores the information about the __winner of the game
        self.__winner: (None, int) = None  # Initially set to None since there is no winner

        # This stores the current move that is to be performed
        # move = 1 indicates that move 1 is to be played now
        self.__move: int = 1

        # Stores the values that are to be highlighted after the game
        self.__highlight_list: List[int] = list()

    def __repr__(self) -> str:
        return self.board

    @property
    def board_list(self) -> List[int]:
        """
        List containing the status of the board (Row Major Order)
        :return: A (duplicate) list of the board list
        """
        return self._board_list[:]

    @property
    def status(self) -> bool:
        """
        :return: The status of the game
        """
        return self.__status

    @property
    def move(self) -> int:
        """
        :return: The current move going on in the game
        """
        return self.__move

    @property
    def turn(self) -> int:
        """
        :return: Which player has to move
        """
        return 1 if self.__move % 2 == 1 else 2

    @property
    def winner(self) -> int:
        """
        :return: The winner of the game, None if no winner
        """
        # !TODO Issue a Warning if there is no winner
        if self.status:
            pass  # Issue a warning here
        return self.__winner

    @property
    def empty_positions(self) -> List[int]:
        """
        :return: A (duplicate) list (in row major order from 0) of the empty positions
        """
        return self._empty_positions[:]

    @property
    def empty_corners(self) -> List[int]:
        """
        :return: A (duplicate) list of the empty corners
        """
        return [i for i in self._empty_positions if i != 4 and i % 2 == 0]

    @property
    def empty_edges(self) -> List[int]:
        """
        :return: A (duplicate) list of the empty corners
        """
        return [i for i in self._empty_positions if i % 2 == 1]

    @property
    def highlighted(self) -> List[int]:
        """
        :return: A (duplicate) list of the positions which must be highlighted
        """
        return self.__highlight_list[:]

    # Some functions for printing the board

    @property
    def board(self) -> str:
        pr_str = ' _____ _____ _____\n'
        for i in range(3):
            pr_str += '|     |     |     |\n|'
            for j in range(3):
                pos_val = self._board_list[i * 3 + j]
                pr_str += f'  {self.__class__._INDICATOR[pos_val]}  |'
            pr_str += '\n|_____|_____|_____|\n'
        return pr_str

    def print_board(self) -> None:
        print(self.board)

    # Helper Functions

    # Raises an error if the status is not true
    def _verify_status(self) -> None:
        if not self.__status:
            raise ZTGameException("Game is not in progress")

    # Raises an error if pos is not empty
    def _verify_pos(self, pos: int) -> None:
        if not self._board_list[pos] == 0:
            raise ZTGameException("Position Already Taken")

    # Returns True if a tuple of board _empty_positions does not contain an empty position
    def __is_fully_played(self, _line: Tuple[int, int, int]) -> bool:
        for pos in _line:
            if self._board_list[pos] == 0:
                return False
        return True

    # Returns true if some player wins
    def __check_win(self, pos: int) -> bool:
        if self.__move < 5:
            return False

        winning_set_list = [pos]
        for line in ZTBaseBoard.LINES[pos]:
            line_val = self._board_list[pos] + \
                       self._board_list[line[0]] + self._board_list[line[1]]

            if line_val in (3 * ZTBaseBoard._VAL_PLAYER1, 3 * ZTBaseBoard._VAL_PLAYER2):
                winning_set_list.extend(line)

        if len(winning_set_list) > 1:
            self.__highlight_list = winning_set_list
            return True

        return False

    # Player Moves

    def __play_player_move(self, player: int, pos: int) -> bool:
        self._verify_status()
        self._verify_pos(pos)

        if self.__move % 2 != player % 2:
            raise ZTGameException("It is currently not the player's move")

        self._board_list[pos] = ZTBaseBoard._VAL_PLAYER1 if player == 1 else ZTBaseBoard._VAL_PLAYER2
        self.on_move(player, pos)
        self._empty_positions.remove(pos)
        self._history.append(pos)

        win = self.__check_win(pos)
        self.__move += 1  # Increasing the move by 1
        return win

    # Handles what happens when player 1 makes a move at position pos
    def _play_player_one_move(self, pos: int) -> None:
        win = self.__play_player_move(1, pos)

        if win:
            self.__finisher(1)  # Player 1 wins
        elif self.__move == 10:
            self.__finisher(0)  # No one Wins and 0 is a draw

    # Handles what happens when player 2 makes a move at position pos
    def _play_player_two_move(self, pos: int) -> None:
        win = self.__play_player_move(2, pos)

        if win:
            self.__finisher(2)

    # Final Function that is called when the game is over
    def __finisher(self, winner: int) -> None:
        self.__winner = winner
        self.__status = False
        self.on_finish()

    def on_move(self, player: int, pos: int) -> None:
        pass

    def on_finish(self) -> None:
        pass
