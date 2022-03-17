from pyfiglet import Figlet

from .io import PlayTicTacToe


def TTTinTerminal(
    board_size: int = 3,
    verbose: bool = True,
    delim: str = ':',
    figlet_font: str = 'big'
) -> None:
    '''
    Play Tic-tac-toe in the terminal (human vs. human)

    Arguments:

    + `board_size`: int (default 3), the board size
    + `verbose`: bool (default `True`), whether to print to the stdout
    + `delim`: str (default ':'), the coordinates delimeter
    + `figlet_font`: str (default 'big'), the font to use when formatting prompts

    Returns: `None`

    The default board is of 3x3 shape. In order to make a move,
    one should write a combination of numbers (X and Y coordinates)
    separated by a delimeter (`delim` argument)

    The text written into the terminal is pretty-formatted with figlet,
    one may specify the desired font via `figlet_font` argument
    '''

    def iter_board_rows(board):
        for i in range(0, board_size**2, board_size):
            from_ = i
            to_ = i + board_size
            yield board[from_:to_]

    formatter = Figlet(font='colossal')
    prompt_formatter = Figlet(font=figlet_font, width=200)
    empty_handler = lambda text: ' ' * 4 if text is None else text

    marks = ('X', 'O')
    prompts = (f'Player {mark} moves (X, Y):\t' for mark in marks)
    prompts = (prompt_formatter.renderText(prompt) for prompt in prompts)

    def on_move(board):
        if not verbose: return
        for row in iter_board_rows(board):
            board = map(empty_handler, row)
            board = ' | '.join(board)
            text = formatter.renderText(board)
            print(text)

    def on_win(winner):
        if not verbose: return
        winner = prompt_formatter.renderText(f'Player {winner} Wins!')
        print(winner)

    def on_start():
        if not verbose: return
        welcome_text = prompt_formatter.renderText('Tic Tac Toe Game!')
        print(welcome_text)

    def on_error(state):
        if state: return
        error_text = 'Bad input!'
        print(prompt_formatter.renderText(error_text))

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