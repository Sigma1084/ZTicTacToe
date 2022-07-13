
"""
pvc_cli.py
===========

The following program is an example of how to use the PvC class of the zttt module.
"""


# Example
def main():
    from zttt import PvC
    from zttt.zt_errors import ZTInvalidInput, ZTError

    # Create a PvP game object
    game = PvC(True)
    game.on_move = lambda player, pos: print(f'{"Player" if game.turn == 2 else "Engine"} played position {pos}')
    game.on_finish = lambda winner: print(f'{"Player" if winner == 2 else "Engine"} won!') if winner \
        else print("It's a draw!")

    # Make a move
    while game.status:
        print(game.board)
        print(f"Empty Positions: {game.empty_positions}")
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
