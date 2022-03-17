from io import StringIO

import pytest

from utils import console as c, tictactoe as t, io as io


@pytest.fixture
def make_factory_params():
    return dict(prompt="some prompt", delim=":", mark="some mark")


@pytest.fixture
def make_buffers():
    return StringIO("0: 3\nBad input\n 1: 2"), StringIO()


def test_default_user_action_factory(make_factory_params, make_buffers):
    in_stream, out_stream = make_buffers

    params = make_factory_params

    action = io.default_user_action_factory(
        in_stream=in_stream, out_stream=out_stream, **params
    )

    assert callable(action)

    x, y, mark = action()
    # i observed a funny fact that StringIO's are acting
    # weirdly when given as streams to the action factory
    assert x == 0 and y == 3 and mark == params["mark"]
    assert out_stream.getvalue() == params["prompt"]

    x, y, mark = action()
    assert x == -1 and y == -1 and mark == params["mark"]
    assert out_stream.getvalue() == params["prompt"] * 2

    x, y, mark = action()
    assert x == 1 and y == 2 and mark == params["mark"]
    assert out_stream.getvalue() == params["prompt"] * 3


def test_TicTacToe():
    board_size = 3.1415
    with pytest.raises(TypeError) as exc_info:
        ttt = t.TicTacToe(board_size=board_size)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, TypeError)

    board_size = 3

    ttt = t.TicTacToe(board_size=board_size)
    assert ttt.board_size == board_size
    assert len(ttt.board) == board_size**2
    assert ttt.winner is None


def test_default_error_handler():
    assert io.default_error_handler(True) is None

    with pytest.raises(ValueError) as exc_info:
        io.default_error_handler(False)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, ValueError)


def test_PlayTicTacToe(make_buffers, make_factory_params):
    '''
    Check that the game can check the arguments provided,
    and actually starts. In this test suite, there will be
    no actual input thus to avoid falling into infinite loop,
    the `on_error` callback raises `RuntimeError`
    moreover, thus we can check that the callback is actually called
    '''
    started = False
    finished = False

    # create some test callbacks
    # make use of nonlocal variables as flags
    def on_start():
        nonlocal started
        started = True

    def on_win(someone):
        nonlocal finished
        finished = True

    def on_error(status): raise RuntimeError

    # in the actual code one would like to print the state
    # of the board somewhere, but here nothing is done
    on_move = lambda board: None

    in_stream, out_stream = make_buffers

    action = io.default_user_action_factory(
        in_stream=in_stream, out_stream=out_stream, **make_factory_params
    )

    # some arbitrary arguments
    marks = ("X", "Y")
    board_size = 3

    # in the following example, neither set of prompts
    # nor actual actions are provided, thus the actions cannot be created
    # automatically via `default_user_action_factory`
    with pytest.raises(TypeError) as exc_info:
        io.PlayTicTacToe(
            board_size=board_size,
            on_start=on_start,
            on_move=on_move,
            on_win=on_win,
            on_error=on_error,
            marks=marks,
            on_action=None,
            prompts=None,
        )

    exception_raised = exc_info.value
    assert isinstance(exception_raised, TypeError)

    assert not started
    assert not finished

    # provide some actual `on_move` function
    with pytest.raises(RuntimeError) as exc_info:
        io.PlayTicTacToe(
            board_size=board_size,
            on_start=on_start,
            on_move=on_move,
            on_win=on_win,
            on_error=on_error,
            marks=marks,
            on_action=(action,),
            prompts=None,
        )

    exception_raised = exc_info.value
    assert isinstance(exception_raised, RuntimeError)

    assert started
    assert not finished
