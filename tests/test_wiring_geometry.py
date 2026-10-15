import pytest

from ursoaia_edu_online.wiring import parse_step, pin_position, rotate_point, route_points


def test_parse_step_horizontal_and_vertical():
    assert parse_step("h30") == (30.0, 0.0)
    assert parse_step("v-12.5") == (0.0, -12.5)


@pytest.mark.parametrize("bad", ["x10", "h", "v1e3", "*", ""])
def test_parse_step_rejects_garbage(bad):
    with pytest.raises(ValueError):
        parse_step(bad)


def test_route_without_steps_goes_horizontal_then_vertical():
    assert route_points((0, 0), (10, 20), []) == [(0, 0), (10, 0), (10, 20)]


def test_route_straight_line_has_no_extra_points():
    assert route_points((0, 5), (40, 5), []) == [(0, 5), (40, 5)]


def test_route_head_steps_from_source():
    assert route_points((0, 0), (50, -30), ["v-30"]) == [(0, 0), (0, -30), (50, -30)]


def test_route_tail_steps_end_in_target():
    # după "*": h50 trebuie să fie ultimul segment, care intră în pin
    pts = route_points((0, 0), (100, 60), ["v40", "*", "h50"])
    assert pts == [(0, 0), (0, 40), (50, 40), (50, 60), (100, 60)]


def test_rotate_point_clockwise_on_screen():
    assert rotate_point((10, 0), (0, 0), 90) == (0, 10)
    assert rotate_point((10, 0), (0, 0), 0) == (10, 0)


def test_pin_position_unrotated():
    part = {"top": 100, "left": 50}
    assert pin_position(part, (40, 60), (5, 7)) == (55, 107)


def test_pin_position_rotated_90_around_center():
    # piesă 40x20 la (0,0), centru (20,10); pinul (0,10) (stânga-mijloc) ajunge sus-mijloc
    part = {"top": 0, "left": 0, "rotate": 90}
    assert pin_position(part, (40, 20), (0, 10)) == (20, -10)
