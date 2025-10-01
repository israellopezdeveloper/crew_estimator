from typing import Any

import pytest

from crew_estimator.estimator import Number, estimate_crew


@pytest.mark.parametrize(
    "volume_cuft, bulky_count, stair_flights, long_distance, expected",
    [
        # --- Volume threshold tests ---
        (480, 0, 0, False, 2),  # Exactly at threshold → base crew of 2
        (481, 0, 0, False, 3),  # Just above threshold → +1 crew for volume
        # --- Bulky items threshold tests ---
        (0, 0, 0, False, 2),  # No bulky items → base crew only
        (0, 1, 0, False, 2),  # 1 bulky item → still no extra crew (0–1 range)
        (0, 2, 0, False, 3),  # 2 bulky items → +1 crew
        (0, 3, 0, False, 3),  # 3 bulky items → still in 2–3 range → +1 crew
        (0, 4, 0, False, 4),  # 4 bulky items → +2 crew
        (0, 5, 0, False, 4),  # 5 bulky items → still in 4–5 range → +2 crew
        # --- Stair flights threshold tests ---
        (0, 0, 2, False, 2),  # 2 flights → below cutoff → no extra crew
        (0, 0, 3, False, 3),  # 3 flights → at cutoff → +1 crew
        # --- Long distance tests ---
        (0, 0, 0, True, 3),  # Long distance flag set → +1 crew
        # --- Mixed edge cases ---
        (480, 1, 3, True, 4),  # Volume not over threshold, +stairs, +distance
        (481, 1, 3, True, 5),  # Volume over threshold, +stairs, +distance
        (481, 0, 3, False, 4),  # Volume over threshold, +stairs only
        (480, 0, 3, False, 3),  # Volume not over, +stairs only
        # --- Explicit test case from prompt ---
        (550, 3, 2, False, 4),  # Expected output from instructions → 4
        # --- Stress test with many bulky items ---
        (
            0,
            99,
            0,
            False,
            2 + 99 // 2,
        ),  # 99 bulky items → 49 extra crew → total 51
    ],
)
def test_estimate_crew_edge_cases(
    volume_cuft: Number,
    bulky_count: int,
    stair_flights: int,
    long_distance: bool,
    expected: int,
) -> None:
    """Check all edge cases and verify the expected crew size is returned."""
    assert (
        estimate_crew(volume_cuft, bulky_count, stair_flights, long_distance)
        == expected
    )


def test_monotonicity_incremental() -> None:
    """
    Monotonicity check: increasing any factor
        (volume, bulky items, stairs, distance)
    should never reduce the calculated crew size.
    """
    base: int = estimate_crew(480, 1, 2, False)  # baseline case = 2 crew

    # Increasing volume above threshold should not decrease crew
    assert estimate_crew(481, 1, 2, False) >= base

    # Increasing bulky items across threshold should not decrease crew
    assert estimate_crew(480, 2, 2, False) >= base

    # Increasing stair flights across cutoff should not decrease crew
    assert estimate_crew(480, 1, 3, False) >= base

    # Enabling long distance flag should not decrease crew
    assert estimate_crew(480, 1, 2, True) >= base


@pytest.mark.parametrize(
    "kwargs, err_msg",
    [
        # ----- volume_cuft invalid -----
        pytest.param(
            {
                "volume_cuft": -0.1,
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": False,
            },
            r"volume_cuft must be a non-negative, finite number",
            id="volume-negative-float",
        ),
        pytest.param(
            {
                "volume_cuft": "big",
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": False,
            },
            r"volume_cuft must be a non-negative, finite number",
            id="volume-wrong-type-str",
        ),
        pytest.param(
            {
                "volume_cuft": float("nan"),
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": False,
            },
            r"volume_cuft must be a non-negative, finite number",
            id="volume-NaN",
        ),
        pytest.param(
            {
                "volume_cuft": float("inf"),
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": False,
            },
            r"volume_cuft must be a non-negative, finite number",
            id="volume-infinity",
        ),
        # ----- bulky_count invalid -----
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": -1,
                "stair_flights": 0,
                "long_distance": False,
            },
            r"bulky_count must be a non-negative integer",
            id="bulky-negative",
        ),
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 2.5,
                "stair_flights": 0,
                "long_distance": False,
            },
            r"bulky_count must be a non-negative integer",
            id="bulky-non-integer-float",
        ),
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": "3",
                "stair_flights": 0,
                "long_distance": False,
            },
            r"bulky_count must be a non-negative integer",
            id="bulky-wrong-type-str",
        ),
        # ----- stair_flights invalid -----
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 0,
                "stair_flights": -3,
                "long_distance": False,
            },
            r"stair_flights must be a non-negative integer",
            id="stairs-negative",
        ),
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 0,
                "stair_flights": 1.2,
                "long_distance": False,
            },
            r"stair_flights must be a non-negative integer",
            id="stairs-non-integer-float",
        ),
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 0,
                "stair_flights": "2",
                "long_distance": False,
            },
            r"stair_flights must be a non-negative integer",
            id="stairs-wrong-type-str",
        ),
        # ----- long_distance invalid -----
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": "yes",
            },
            r"long_distance must be a boolean",
            id="long-distance-str",
        ),
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": 1,
            },
            r"long_distance must be a boolean",
            id="long-distance-int",
        ),
        pytest.param(
            {
                "volume_cuft": 100.0,
                "bulky_count": 0,
                "stair_flights": 0,
                "long_distance": None,
            },
            r"long_distance must be a boolean",
            id="long-distance-none",
        ),
    ],
)
def test_invalid_inputs_raise_value_error(
    kwargs: dict[str, Any],
    err_msg: str,
) -> None:
    """
    All invalid inputs must raise ValueError with a clear, specific message.
    """
    print("HOLA")
    with pytest.raises(ValueError, match=err_msg):
        estimate_crew(**kwargs)
