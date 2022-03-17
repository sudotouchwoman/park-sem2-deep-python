from sys import stdin, stdout
from io import StringIO

from .tictactoe import TicTacToe


def default_user_action_factory(
    prompt: str,
    delim: str,
    mark,
    in_stream: StringIO = stdin,
    out_stream: StringIO = stdout
):
    def default_action():
        print(prompt, file=out_stream)
        try: x, y = map(int, in_stream.readline().split(delim))
        except ValueError: return -1, -1, mark
        else: return x, y, mark

    return default_action


def default_error_handler(state):
    if not state: raise ValueError(f"The input provided is invalid")


def PlayTicTacToe(
    board_size,
    marks,
    on_start,
    on_move,
    on_win,
    on_error=default_error_handler,
    on_action=None,
    prompts=None,
    delim: str = ':',
):
    if prompts is None and on_action is None:
        raise ValueError(f'Should provide a set of either prompts or actions')

    actions = (
        default_user_action_factory(prompt, delim, mark)
        for prompt, mark in zip(prompts, marks)
    ) if on_action is None else on_action

    game = TicTacToe(board_size, *actions)
    on_start()

    for board, state in game.play():
        on_move(board)
        on_error(state)

    on_win(game.winner)    
