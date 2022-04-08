from .io import PlayTicTacToe


def TTTinTerminal(
    board_size: int = 3,
    verbose: bool = True,
    delim: str = ':',
) -> None:
    '''
    Play Tic-tac-toe in the terminal (human vs. human)

    Arguments:

    + `board_size`: int (default 3), the board size
    + `verbose`: bool (default `True`), whether to print to the stdout
    + `delim`: str (default ':'), the coordinates delimeter

    Returns: `None`

    The default board is of 3x3 shape. In order to make a move,
    one should write a combination of numbers (X and Y coordinates)
    separated by a delimeter (`delim` argument)
    '''

    def iter_board_rows(board):
        for i in range(0, board_size**2, board_size):
            from_ = i
            to_ = i + board_size
            yield board[from_:to_]

    empty_handler = lambda text: ' ' * 1 if text is None else text

    marks = ('X', 'O')
    prompts = (f'\nPlayer {mark} moves (X, Y):\t' for mark in marks)

    def on_move(board):
        if not verbose: return
        for row in iter_board_rows(board):
            board = map(empty_handler, row)
            print(' | '.join(board))

    def on_win(winner):
        if not verbose: return
        print('We have a draw!' if winner is None else f'Player {winner} Wins!')

    def on_start():
        if not verbose: return
        welcome_text = 'Tic Tac Toe Game!'
        print(welcome_text)

    def on_error(state):
        if state: return
        error_text = 'Bad input!'
        print(error_text)

    PlayTicTacToe(
        board_size=board_size,
        marks=marks,
        prompts=prompts,
        on_start=on_start,
        on_move=on_move,
        on_win=on_win,
        on_error=on_error,
        delim=delim
    )
