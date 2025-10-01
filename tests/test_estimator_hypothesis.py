from hypothesis import given
from hypothesis import strategies as st

from crew_estimator.estimator import Number, estimate_crew

# ---------- Strategies ----------
# volume_cuft: finite and >= 0 (int or float)
volume_strat = st.one_of(
    st.integers(min_value=0, max_value=10000),
    st.floats(
        min_value=0.0,
        max_value=10000.0,
        allow_nan=False,
        allow_infinity=False,
    ),
)
# bulky_count and stair_flights: valid ints
bulky_strat = st.integers(min_value=0, max_value=10000)
stairs_strat = st.integers(min_value=0, max_value=1000)
bool_strat = st.booleans()


def spec_model(
    volume_cuft: Number,
    bulky_count: int,
    stair_flights: int,
    long_distance: bool,
) -> int:
    """Reference model from the business rules."""
    crew: int = 2
    if volume_cuft > 480:
        crew += 1
    crew += bulky_count // 2
    if stair_flights >= 3:
        crew += 1
    if long_distance:
        crew += 1
    return crew


@given(
    volume=volume_strat,
    bulky=bulky_strat,
    stairs=stairs_strat,
    long=bool_strat,
)
def test_matches_spec_model(
    volume: Number,
    bulky: int,
    stairs: int,
    long: bool,
) -> None:
    """Output must exactly match the spec model for all generated inputs."""
    assert estimate_crew(volume, bulky, stairs, long) == spec_model(
        volume, bulky, stairs, long
    )


@given(
    base_volume=volume_strat,
    bulky=bulky_strat,
    stairs=stairs_strat,
    long=bool_strat,
    delta=st.floats(
        min_value=0.0, max_value=1000.0, allow_nan=False, allow_infinity=False
    ),
)
def test_monotonicity_volume(
    base_volume: Number,
    bulky: int,
    stairs: int,
    long: bool,
    delta: float,
) -> None:
    """Increasing volume must not decrease the crew."""
    v1, v2 = base_volume, base_volume + delta
    c1 = estimate_crew(v1, bulky, stairs, long)
    c2 = estimate_crew(v2, bulky, stairs, long)
    assert c2 >= c1


@given(
    volume=volume_strat,
    base_bulky=bulky_strat,
    stairs=stairs_strat,
    long=bool_strat,
)
def test_monotonicity_bulky(
    volume: Number,
    base_bulky: int,
    stairs: int,
    long: bool,
) -> None:
    """Adding one bulky item must not decrease the crew."""
    c1 = estimate_crew(volume, base_bulky, stairs, long)
    c2 = estimate_crew(volume, base_bulky + 1, stairs, long)
    assert c2 >= c1


@given(
    volume=volume_strat,
    bulky=bulky_strat,
    base_stairs=stairs_strat,
    long=bool_strat,
)
def test_monotonicity_stairs(
    volume: Number,
    bulky: int,
    base_stairs: int,
    long: bool,
) -> None:
    """Increasing stair flights must not decrease the crew."""
    c1 = estimate_crew(volume, bulky, base_stairs, long)
    c2 = estimate_crew(volume, bulky, base_stairs + 1, long)
    assert c2 >= c1


@given(volume=volume_strat, bulky=bulky_strat, stairs=stairs_strat)
def test_long_distance_adds_one(
    volume: Number,
    bulky: int,
    stairs: int,
) -> None:
    """Long-distance flag adds exactly +1 to the crew."""
    assert (
        estimate_crew(volume, bulky, stairs, True)
        == estimate_crew(volume, bulky, stairs, False) + 1
    )


@given(
    volume=volume_strat,
    base_bulky=bulky_strat,
    stairs=stairs_strat,
    long=bool_strat,
)
def test_bulky_step_function(
    volume: Number,
    base_bulky: int,
    stairs: int,
    long: bool,
) -> None:
    """
    Bulky contribution is floor(bulky/2): 2k -> 2k+1 (same), 2k+1 -> 2k+2 (+1).
    """
    even = base_bulky - (base_bulky % 2)  # 2k
    c_even = estimate_crew(volume, even, stairs, long)
    c_odd = estimate_crew(volume, even + 1, stairs, long)
    c_next = estimate_crew(volume, even + 2, stairs, long)
    assert c_odd == c_even
    assert c_next == c_odd + 1
