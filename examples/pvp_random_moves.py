"""examples/pvp_random_moves.py"""


def main():
    from zttt import PvP
    from random import choice

    # Create a PvP game object
    game = PvP()
    game.on_move = lambda player, pos: print(f'Player {player} played position {pos}')
    game.on_finish = lambda winner: print(f'Player {winner} won!') if winner else print("It's a draw!")

    # Make a move
    while game.status:
        print(f"It is Player {game.turn}'s turn")
        game.play(choice(game.empty_positions))
        print(game.board)

    # game.empty_positions: List of empty positions on the board
    # game.turn: The player whose turn it is

    print("Positions to be highlighted", game.highlighted)


if __name__ == '__main__':
    main()
