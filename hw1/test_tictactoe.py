from io import StringIO

import pytest

from utils import console as c, tictactoe as t, io as io


@pytest.fixture
def factory_params():
    return dict(prompt="some prompt\n", delim=":", mark="some mark")


def test_default_user_action_factory(factory_params):
    in_stream = StringIO('0: 3\nBad input\n 1: 2')
    out_stream = StringIO()

    action = io.default_user_action_factory(
        in_stream=in_stream, out_stream=out_stream, **factory_params
    )

    assert callable(action)

    x, y, mark = action()
    assert x == 0 and y == 3 and mark == factory_params['mark']
    assert out_stream.readline() == factory_params['prompt']

    x, y, mark = action()
    assert x == -1 and y == -1 and mark == factory_params['mark']
    assert out_stream.readline() == factory_params['prompt']

    x, y, mark = action()
    assert x == 1 and y == 2 and mark == factory_params['mark']
    assert out_stream.readline() == factory_params['prompt']


def test_TicTacToe():
    board_size = 3.1415
    with pytest.raises(TypeError) as exc_info:
        ttt = t.TicTacToe(board_size=board_size)

    exception_raised = exc_info.value
    assert isinstance(exception_raised, TypeError)

    board_size = 3

    ttt = t.TicTacToe(board_size=board_size)
    assert ttt.board_size == board_size
    assert len(ttt.board) == board_size ** 2
    assert ttt.winner is None

