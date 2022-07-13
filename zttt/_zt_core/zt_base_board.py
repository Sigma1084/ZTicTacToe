from typing import List, Tuple, Dict, Callable, Iterable, Any, Union
from ..zt_errors import ZTGameException, ZTInvalidInput


class ZTBaseBoard:
    """This is the base class which is inherited by all the classes which are used in the module"""

    # The following variables are not to be changed
    _VAL_PLAYER1 = 4  # Value for player 1 in the board_list
    _VAL_PLAYER2 = 1  # Value for player 2 in the board_list
    _VAL_EMPTY = 0  # Value for empty position in the board_list

    # Indicates what the values contained in the _board_list represent
    # The indicator with value 5 goes first
    _INDICATOR: Dict[int, str] = {
        _VAL_PLAYER1: 'X',
        _VAL_PLAYER2: 'O',
        _VAL_EMPTY: ' '
    }

    # All the lines the current position
    _LINES: Dict[int, List[Tuple[int, int]]] = {
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
    def set_indicators(cls, _player1: str = 'X', _player2: str = 'O', _space: str = ' ') -> None:
        """Sets the indicators, a class method

        :param _player1: Indicator for player 1
        :type _player1: str
        :param _player2: Indicator for player 2
        :type _player2: str
        :param _space: Indicator for empty position
        :type _space: str
        :return: None
        """

        cls._INDICATOR = {
            cls._VAL_PLAYER1: str(_player1),
            cls._VAL_PLAYER2: str(_player2),
            cls._VAL_EMPTY: str(_space)
        }

    def __init__(self) -> None:
        """Initializes the board and the state variables"""

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

        # Event triggers
        self._on_move: Callable[[int, int], None] = lambda player, pos: None
        self._on_finish: Callable[[int], None] = lambda player: None

        # Used for function calls
        self._data: Dict[str, Any] = {'args': list(), 'kwargs': dict(), 'output': None}

    # Useful properties

    @property
    def board_list(self) -> List[int]:
        """List containing the status of the board (Row Major Order)

        :return: A (duplicate) list of the board list
        :rtype: List[int]
        """
        return self._board_list[:]

    @property
    def status(self) -> bool:
        """Whether the game is in progress or not

        :return: The status of the game
        :rtype: bool
        """
        return self.__status

    @property
    def move(self) -> int:
        """The current move that is to be performed

        :return: Current Move Number
        :rtype: int
        """
        return self.__move

    @property
    def turn(self) -> int:
        """The player whose turn it is to play

        :return: Player Number
        :rtype: int
        """
        return 1 if self.__move % 2 == 1 else 2

    @property
    def winner(self) -> (None, int):
        """The winner of the game

        :return: Winner if the game is over, 0 is draw, None if no winner yet
        :rtype: (None, int)
        """
        # !TODO Issue a Warning if there is no winner
        if self.status:
            pass  # Issue a warning here
        return self.__winner

    @property
    def history(self) -> List[int]:
        """Returns the history of the game

        :return: A (duplicate) list of the history
        :rtype: List[int]
        """
        return self._history[:]

    @property
    def empty_positions(self) -> List[int]:
        """Returns the list of empty positions

        :return: A (duplicate) list (in row major order from 0) of the empty positions
        :rtype: List[int]
        """
        return self._empty_positions[:]

    @property
    def empty_corners(self) -> List[int]:
        """Returns the list of empty corners

        :return: List of the empty corners
        :rtype: List[int]
        """
        return [i for i in self._empty_positions if i is not self._CENTER and i % 2 == 0]

    @property
    def empty_edges(self) -> List[int]:
        """Returns the list of empty edges

        :return: List of the empty edges
        :rtype: List[int]
        """
        return [i for i in self._empty_positions if i % 2 == 1]

    @property
    def highlighted(self) -> List[int]:
        """Returns the highlighted positions of the board when there is a winner, empty list otherwise

        :return: A (duplicate) list of highlighted positions
        :rtype: List[int]
        """
        return self.__highlight_list[:]

    @property
    def board(self) -> str:
        """Returns the string representation of the board

        :return: board string
        :rtype: str
        """

        pr_str = ' _____ _____ _____\n'
        for i in range(3):
            pr_str += '|     |     |     |\n|'
            for j in range(3):
                pos_val = self._board_list[i * 3 + j]
                pr_str += f'  {self.__class__._INDICATOR[pos_val]}  |'
            pr_str += '\n|_____|_____|_____|\n'
        return pr_str

    # Triggers Setup

    @property
    def on_move(self) -> Callable[[int, int], None]:
        """Returns the on_move event trigger

        :return: on_move event trigger
        :rtype: Callable[[int, int], None]
        """
        return self._on_move

    @on_move.setter
    def on_move(self, _on_move: Callable[[int, int], None]) -> None:
        """Sets the on_move event trigger

        :param _on_move: The on_move callable
        :type _on_move: Callable[[int, int], None]
        :raise: TypeError if on_move is not a callable
        """

        if not callable(_on_move):
            raise TypeError('on_move must be a function')
        self._on_move = _on_move

    @property
    def on_finish(self) -> Callable[[int], None]:
        """Returns the on_move event trigger

        :return: _on_finish event trigger
        :rtype: Callable[[int], None]
        """
        return self._on_finish

    @on_finish.setter
    def on_finish(self, _on_finish: Callable[[int], None]) -> None:
        """Sets the on_move event trigger

        :param _on_finish: The on_finish callable
        :type _on_finish: Callable[[int], None]
        :raise: TypeError if on_finish is not a callable
        """

        if not callable(_on_finish):
            raise TypeError('on_move must be a function')
        self._on_finish = _on_finish

    # Helper Functions

    def _verify_status(self) -> None:
        """Raises an error if the status is not true

        :raise: ZTGameException if the status is False
        """
        if not self.__status:
            raise ZTGameException("Game is not in progress")

    def _verify_pos(self, pos: int) -> None:
        """Raises an error if pos is not empty

        :param pos: The position to be verified
        :type pos: int
        :raise: ZTInvalidInput if the position is not empty or if the input is wrong
        """

        try:
            pos = int(pos)
        except ValueError:
            raise ZTInvalidInput("Position entered must be an integer")
        except Exception as e:
            print(f"Unknown Error while verifying the position {pos}. Please raise an issue.")
            raise ZTInvalidInput(e)

        if pos not in self._empty_positions:
            raise ZTInvalidInput("Invalid Position Entered")

        if not self._board_list[pos] == 0:
            raise ZTInvalidInput("Position Already Taken")

    def __is_fully_played(self, _line: Tuple[int, int, int]) -> bool:
        """Checks if the given line is fully played

        :param _line: A tuple of three positions
        :type _line: Tuple[int, int, int]
        :return: True if the tuple of positions is fully played, False otherwise
        :rtype: bool
        """

        for pos in _line:
            if self._board_list[pos] == 0:
                return False
        return True

    def __check_win(self, pos: int) -> bool:
        """Checks if a player won after the current move

        :param pos: The position that was just played
        :type pos: int
        :return: True if the player won, False otherwise
        :rtype: bool
        """

        if self.__move < 5:
            return False

        winning_set_list = [pos]
        for line in ZTBaseBoard._LINES[pos]:
            line_val = self._board_list[pos] + \
                       self._board_list[line[0]] + self._board_list[line[1]]

            if line_val in (3 * ZTBaseBoard._VAL_PLAYER1, 3 * ZTBaseBoard._VAL_PLAYER2):
                winning_set_list.extend(line)

        if len(winning_set_list) > 1:
            self.__highlight_list = winning_set_list
            return True

        return False

    def __finisher(self, winner: int) -> None:
        """Function for handling the end of the game

        :param winner: The winner of the game
        :type winner: int
        :return: None
        """

        self.__winner = winner
        self.__status = False
        self.on_finish(winner)

    # Player Moves

    def __play_player_move(self, player: int, pos: int) -> bool:
        """Plays a move for the player at the given position

        :param player: The player who is making the move
        :type player: int
        :param pos: The position to be played
        :type pos: int
        :return: True if there was a winner, False otherwise
        :rtype: bool
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        self._verify_status()
        self._verify_pos(pos)
        pos = int(pos)

        if self.__move % 2 != player % 2:
            raise ZTGameException("It is currently not the player's move")

        self._board_list[pos] = ZTBaseBoard._VAL_PLAYER1 if player == 1 else ZTBaseBoard._VAL_PLAYER2
        self._empty_positions.remove(pos)
        self._history.append(pos)

        # self._data['out'] = self.on_move(player, pos, *self._data['args'], **self._data['kwargs'])
        self.on_move(player, pos)

        win = self.__check_win(pos)
        self.__move += 1  # Increasing the move by 1
        return win

    def _play_player_one_move(self, pos: int) -> None:
        """Function for handling the player 1 move

        :param pos: The position to be played
        :type pos: int
        :return: None
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        win = self.__play_player_move(1, pos)

        if win:
            self.__finisher(1)  # Player 1 wins
        elif self.__move == 10:
            self.__finisher(0)  # No one Wins and 0 is a draw

    def _play_player_two_move(self, pos: int) -> None:
        """Function for handling the player 2 move

        :param pos: The position to be played
        :type pos: int
        :return: None
        :raise: ZTGameException if the game is not in progress
        :raise: ZTInvalidInput if the move is invalid
        """

        win = self.__play_player_move(2, pos)

        if win:
            self.__finisher(2)
