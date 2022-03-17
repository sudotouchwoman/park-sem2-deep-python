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
    '''
    Create a function to fetch inputs
    from user (in the default case, from the console)
    This function is used in `PlayTicTacToe` when the
    `on_move` argument is not provided
    '''

    def default_action():
        out_stream.write(prompt)
        # this implementation does not raise, thus
        # if there is an incorrect input, the user will be prompted
        # to input again
        try: x, y = map(int, in_stream.readline().split(delim))
        except ValueError: return -1, -1, mark
        else: return x, y, mark

    return default_action


def default_error_handler(state):
    # default error handler will raise an exception
    # and the game loop will abort
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
        raise TypeError(f'Should provide a set of either prompts or actions')

    actions = (
        (
            default_user_action_factory(prompt, delim, mark)
            for prompt, mark in zip(prompts, marks)
        )
        if on_action is None
        else on_action
    )

    game = TicTacToe(board_size, *actions)
    on_start()

    for board, state in game.play():
        on_move(board)
        on_error(state)

    on_win(game.winner)    
