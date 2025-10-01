import math

Number = int | float


def estimate_crew(
    volume_cuft: Number,
    bulky_count: int,
    stair_flights: int,
    long_distance: bool,
) -> int:
    if (
        not isinstance(volume_cuft, (int, float))
        or volume_cuft < 0
        or not math.isfinite(volume_cuft)
    ):
        raise ValueError("volume_cuft must be a non-negative, finite number")
    if not isinstance(bulky_count, int) or bulky_count < 0:
        raise ValueError("bulky_count must be a non-negative integer")
    if not isinstance(stair_flights, int) or stair_flights < 0:
        raise ValueError("stair_flights must be a non-negative integer")
    if not isinstance(long_distance, bool):
        raise ValueError("long_distance must be a boolean")

    crew: int = 2
    if volume_cuft > 480:
        crew += 1
    crew += bulky_count // 2
    if stair_flights >= 3:
        crew += 1
    if long_distance:
        crew += 1
    return crew
