"""examples/pvp_cli.py"""


def main():
    from zttt import PvP
    from zttt.zt_errors import ZTInvalidInput, ZTError

    # Create a PvP game object
    game = PvP()
    game.on_move = lambda player, pos: print(f'Player {player} played position {pos}')
    game.on_finish = lambda winner: print(f'Player {winner} won!') if winner else print("It's a draw!")

    # Make a move
    while game.status:
        print(game.board)
        print(f"Empty Positions: {game.empty_positions}")
        print(f"It is Player {game.turn}'s turn. Enter your position")
        print()
        try:
            game.play(input(f"Enter position to play: "))
        except ZTInvalidInput as e:
            print(e, "! Try again", sep='')
        except ZTError as e:
            print("Unknown zttt Exception. Please raise an issue. Try again")
        finally:
            print()

    print(game.board)
    print("Positions to be highlighted", game.highlighted)


if __name__ == '__main__':
    main()
