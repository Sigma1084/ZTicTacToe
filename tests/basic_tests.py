
def test_version():
    from zttt import __version__
    assert __version__ == '0.4.0'


def test_basic_pvc_player_first():
    from zttt import PvC
    b = PvC(False)
    assert b.turn == 1
    b.play(0)
    assert b.board_list == [4, 0, 0, 0, 1, 0, 0, 0, 0]


def test_set_indicators():
    from zttt import PvP
    PvP.set_indicators('O', 'X', '_')
    b = PvP()
    b.play(1)
    b.play(2)
    assert b.board.split('\n')[2] == '|  _  |  O  |  X  |'
    b.set_indicators()
    assert b.board.split('\n')[2] == '|     |  X  |  O  |'


def test_on_move_setter():
    from zttt import PvP
    b = PvP()
    print()
    test_list = []

    def func(player, pos):
        test_list.append(f"Player {player} played at Position {pos}")

    b.on_move = func
    b.play(0)
    b.play(1)
    b.play(2)

    assert test_list[0] == "Player 1 played at Position 0"
    assert test_list[1] == "Player 2 played at Position 1"
    assert test_list[2] == "Player 1 played at Position 2"
    assert b.history == [0, 1, 2]


def test_game_finish():
    from zttt import PvP
    b = PvP()
    out = []
    b.on_finish = lambda winner: out.append(f"Player {winner} WON" if winner else "Draw")
    b.play(0)
    b.play(1)
    b.play(3)
    b.play(2)
    b.play(6)
    assert b.status is False
    assert b.winner is 1
    assert out[0] == "Player 1 WON"


def test_draw():
    from zttt import PvP
    b = PvP()
    out = []
    b.on_finish = lambda winner: out.append(f"Player {winner} WON" if winner else "Draw")
    b.play(1)
    b.play(2)
    b.play(3)
    b.play(4)
    b.play(5)
    b.play(0)
    b.play(6)
    b.play(7)
    b.play(8)
    assert b.status is False
    assert b.winner is 0
    assert out[0] == "Draw"
