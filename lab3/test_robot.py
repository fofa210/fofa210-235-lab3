import pytest

from robot import Robot, Direction, IllegalMoveException


@pytest.fixture
def robot():
    return Robot()


def test_constructor(robot):
    state = robot.state()

    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_east_turn(robot):
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.EAST


def test_south_turn(robot):
    robot.turn()
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.SOUTH


def test_west_turn(robot):
    robot.turn()
    robot.turn()
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.WEST


def test_north_turn(robot):
    robot.turn()
    robot.turn()
    robot.turn()
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.NORTH


def test_illegal_north_move(robot):
    state = robot.state()
    assert state['direction'] == Direction.NORTH

    with pytest.raises(IllegalMoveException):
        while state['row'] > 0:
            robot.move()


def test_illegal_east_move(robot):
    robot.turn()
    state = robot.state()
    assert state['direction'] == Direction.EAST

    with pytest.raises(IllegalMoveException):
        while state['col'] < 10:
            robot.move()


def test_illegal_south_move(robot):
    robot.turn()
    robot.turn()
    state = robot.state()
    assert state['direction'] == Direction.SOUTH

    with pytest.raises(IllegalMoveException):
        robot.move()


def test_illegal_west_move(robot):
    robot.turn()
    robot.turn()
    robot.turn()
    state = robot.state()
    assert state['direction'] == Direction.WEST

    with pytest.raises(IllegalMoveException):
        robot.move()


def test_move_north(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1


def test_move_east(robot):
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 2


def test_move_south(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1
    robot.turn()
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


def test_move_west(robot):
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 2
    robot.turn()
    robot.turn()
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_without_history(robot):
    try:
        robot.back_track()
    except IndexError:
        pass
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_with_move(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1

    robot.back_track()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_with_turn(robot):
    robot.turn()
    state = robot.state()
    assert state['direction'] == Direction.EAST

    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH


def test_back_track_with_multiple_moves(robot):
    robot.move()
    robot.move()
    state = robot.state()
    assert state['row'] == 8
    assert state['col'] == 1

    robot.back_track()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1

def test_back_tracks_with_multiple_moves(robot):
    robot.move()
    robot.move()
    state = robot.state()
    assert state['row'] == 8
    assert state['col'] == 1

    robot.back_track()
    robot.back_track()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1