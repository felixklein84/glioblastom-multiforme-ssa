"""Schedule helpers — windows and pulse breakpoints."""

from gbm_ctmc.therapy.schedule import (
    is_in_any_window,
    pulse_breakpoints_in,
    window_breakpoints_in,
)


def test_is_in_any_window_half_open():
    wins = [(0.0, 5.0), (10.0, 15.0)]
    assert is_in_any_window(0.0, wins) is True
    assert is_in_any_window(4.999, wins) is True
    assert is_in_any_window(5.0, wins) is False    # right edge excluded
    assert is_in_any_window(7.0, wins) is False
    assert is_in_any_window(14.5, wins) is True
    assert is_in_any_window(20.0, wins) is False


def test_window_breakpoints_in_range():
    wins = [(0.0, 5.0), (10.0, 15.0)]
    # Range (0, 10] picks up start of win2 and end of win1 (both in half-open (0,10])
    bps = window_breakpoints_in(wins, 0.0, 10.0)
    assert 5.0 in bps
    assert 10.0 in bps
    # 0.0 itself is excluded (t_lo is strictly less than)
    assert 0.0 not in bps


def test_pulse_breakpoints_in_range():
    times = [1.0, 2.0, 3.0, 10.0]
    assert pulse_breakpoints_in(times, 0.0, 3.0) == [1.0, 2.0, 3.0]
    assert pulse_breakpoints_in(times, 1.0, 10.0) == [2.0, 3.0, 10.0]
    assert pulse_breakpoints_in(times, 100.0, 200.0) == []
