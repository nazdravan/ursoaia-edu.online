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


def test_route_tail_steps_start_from_target():
    # Wokwi: pașii de după "*" pornesc din destinație (start coadă = destinație + pași),
    # iar golul se închide perpendicular pe pasul de coadă vecin (h → golul se termină vertical)
    pts = route_points((0, 0), (100, 60), ["v40", "*", "h50"])
    assert pts == [(0, 0), (0, 40), (150, 40), (150, 60), (100, 60)]


# Trasee citite din wokwi.com (Arduino UNO, 2026-10-15), colțurile rotunjite ignorate.
@pytest.mark.parametrize("start,end,steps,expected", [
    ((236.5, 9), (208, 191.5), [], [(236.5, 9), (208, 9), (208, 191.5)]),
    ((208, 9), (236.5, 191.5), ["v20"], [(208, 9), (208, 29), (208, 191.5), (236.5, 191.5)]),
    ((125, 9), (179, 191.5), ["h-20"], [(125, 9), (105, 9), (179, 9), (179, 191.5)]),
    ((198.5, 9), (246, 191.5), ["*", "h15"], [(198.5, 9), (261, 9), (261, 191.5), (246, 191.5)]),
    ((189, 9), (255.5, 191.5), ["*", "v15"], [(189, 9), (189, 206.5), (255.5, 206.5), (255.5, 191.5)]),
    ((236.5, 9), (208, 191.5), ["*", "h15", "v15"],
     [(236.5, 9), (223, 9), (223, 206.5), (208, 206.5), (208, 191.5)]),
    ((227, 9), (217.5, 191.5), ["*", "v15", "h15"],
     [(227, 9), (227, 206.5), (232.5, 206.5), (232.5, 191.5), (217.5, 191.5)]),
    ((185, -88), (115.5, 9), ["v60"], [(185, -88), (185, -28), (185, 9), (115.5, 9)]),
])
def test_route_matches_wokwi(start, end, steps, expected):
    assert route_points(start, end, steps) == expected


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
