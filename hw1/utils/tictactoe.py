class TicTacToe:
    '''
    The class to handle everything related to the game,
    i.e. the board and input callbacks

    Arguments:

    + `board_size`: int, the board size
    + `input_callers`, sequence of callable objects, the input callbacks
    '''

    def __init__(self, board_size: int, *input_callers) -> None:
        self.__val_args(board_size, *input_callers)
        self.board_size = board_size
        self.board = [None for _ in range(board_size**2)]
        self.winner = None
        self.input_callers = input_callers

    def play(self):
        '''
        Game loop as a generator
        on each step, yields the board state and the
        result of the last move (whether it was successful or not)
        '''
        yield self.board, True

        has_empty = lambda: None in self.board

        # play while the winner is not found and there
        # still is some empty space on the board
        while self.winner is None and has_empty():
            for caller in self.input_callers:
                state = False
                while not state and has_empty():
                    x, y, mark = caller()
                    state = self.__make_move(x, y, mark)
                    yield self.board, state
                self.winner = self.__game_step()
                # if the winner was actually found
                if self.winner is not None: break

        yield self.board, True

    def __make_move(self, x, y, mark) -> bool:
        if x < 0 or y < 0: return False
        idx = y * self.board_size + x
        try:
            if self.board[idx] is not None: return False
        except IndexError: return False

        self.board[idx] = mark
        return True

    def __game_step(self):
        '''
        Iterate over the board and check all the feasible
        positions on the board (rows, columns and the main diagonals)
        '''
        def iter_rows():
            for i in range(0, self.board_size**2, self.board_size):
                from_ = i
                to_ = i + self.board_size
                yield self.board[from_:to_]

        def iter_cols():
            for i in range(self.board_size):
                yield self.board[i::self.board_size]

        def iter_main_diag():
            for i, cell in enumerate(self.board):
                x, y = divmod(i, self.board_size)
                if x == y: yield cell

        def iter_secondary_diag():
            for i, cell in enumerate(self.board):
                x, y = divmod(i, self.board_size)
                if self.board_size - 1 - x == y: yield cell

        for row in map(set, iter_rows()):
            if len(row) == 1: return min(row)

        for col in map(set, iter_cols()):
            if len(col) == 1: return min(col)

        main_diag, secondary_diag = set(iter_main_diag()), set(iter_secondary_diag())

        if len(main_diag) == 1: return min(main_diag)
        if len(secondary_diag) == 1: return min(secondary_diag)


    def __val_args(self, board_size: int, *input_callers) -> None:
        # validate the arguments provided to the class constructor
        if not isinstance(board_size, int):
            raise TypeError(f"Expected integer board size")
        for i, caller in enumerate(input_callers):
            if callable(caller): continue
            raise TypeError(f"Non-callable argument at position {i}: {caller}")
