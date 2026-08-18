import pytest

from waypoint.domain import (
    Distance,
    Trail,
    DayHike,
    BackpackingRoute,
    TrailRun,
    GuidedDayHike,
    RatedGuidedDayHike,
    FakeTrail,
    print_estimated_times,
)


# ============================================================
# WP-202 — Distance arithmetic
# ============================================================

def test_distance_addition():
    result = Distance(3, "km") + Distance(2, "km")

    assert result == Distance(5, "km")


def test_distance_subtraction():
    result = Distance(5, "km") - Distance(2, "km")

    assert result == Distance(3, "km")


def test_distance_subtraction_rejects_negative_result():
    with pytest.raises(ValueError):
        Distance(2, "km") - Distance(5, "km")


def test_distance_sorting():
    distances = [
        Distance(5, "km"),
        Distance(2, "km"),
        Distance(10, "km"),
        Distance(1, "km"),
    ]

    distances.sort()

    assert distances == [
        Distance(1, "km"),
        Distance(2, "km"),
        Distance(5, "km"),
        Distance(10, "km"),
    ]


def test_distance_greater_than():
    assert Distance(10, "km") > Distance(5, "km")


def test_distance_less_than():
    assert Distance(3, "km") < Distance(5, "km")


# ============================================================
# WP-202 — Mixed units
# ============================================================

def test_mixed_units_are_automatically_converted():
    result = Distance(5, "km") + Distance(1, "mi")

    assert result.unit == "km"
    assert result.magnitude == pytest.approx(
        6.609344,
        rel=1e-6,
    )


def test_mixed_units_preserve_left_operand_unit():
    result = Distance(1, "mi") + Distance(1, "km")

    assert result.unit == "mi"

    assert result.magnitude == pytest.approx(
        1.621371192,
        rel=1e-6,
    )


def test_mixed_unit_comparison():
    assert Distance(1, "mi") > Distance(1, "km")


def test_distance_string():
    distance = Distance(5, "km")

    assert str(distance) == "5 km"


def test_distance_repr():
    distance = Distance(5, "km")

    assert repr(distance) == "Distance(5.0, 'km')"


# ============================================================
# WP-201 — Abstract Trail
# ============================================================

def test_trail_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Trail(
            name="Abstract Trail",
            distance=Distance(5, "km"),
            elevation_gain_m=100,
            difficulty="easy",
        )


def test_missing_abstract_method_cannot_be_instantiated():

    class BrokenTrail(Trail):
        def estimated_time(self):
            return 1

        # summary() intentionally missing

    with pytest.raises(TypeError):
        BrokenTrail(
            name="Broken",
            distance=Distance(5, "km"),
            elevation_gain_m=100,
            difficulty="easy",
        )


# ============================================================
# WP-201 — Trail types
# ============================================================

def test_day_hike_estimated_time():
    trail = DayHike(
        name="Day Hike",
        distance=Distance(10, "km"),
        elevation_gain_m=200,
        difficulty="moderate",
    )

    assert trail.estimated_time() == pytest.approx(2.5)


def test_backpacking_route_estimated_time():
    trail = BackpackingRoute(
        name="Backpacking Route",
        distance=Distance(10, "km"),
        elevation_gain_m=500,
        difficulty="moderate",
        nights=2,
    )

    assert trail.estimated_time() == pytest.approx(
        10 / 3.0
    )


def test_trail_run_estimated_time():
    trail = TrailRun(
        name="Trail Run",
        distance=Distance(10, "km"),
        elevation_gain_m=200,
        difficulty="moderate",
    )

    assert trail.estimated_time() == pytest.approx(
        10 / 7.0
    )


def test_different_trail_types_have_different_pacing():
    distance = Distance(10, "km")

    hike = DayHike(
        "Hike",
        distance,
        100,
        "moderate",
    )

    backpack = BackpackingRoute(
        "Backpack",
        distance,
        100,
        "moderate",
    )

    run = TrailRun(
        "Run",
        distance,
        100,
        "moderate",
    )

    assert hike.estimated_time() != backpack.estimated_time()
    assert backpack.estimated_time() != run.estimated_time()


# ============================================================
# WP-203 — GuidedDayHike
# ============================================================

def test_guided_day_hike_adds_guide():
    trail = GuidedDayHike(
        name="Guided Hike",
        distance=Distance(8, "km"),
        elevation_gain_m=300,
        difficulty="moderate",
        guide_name="Sarah",
    )

    assert trail.guide_name == "Sarah"


def test_guided_day_hike_uses_parent_behavior():
    trail = GuidedDayHike(
        name="Guided Hike",
        distance=Distance(8, "km"),
        elevation_gain_m=300,
        difficulty="moderate",
        guide_name="Sarah",
    )

    # estimated_time() is inherited from DayHike
    assert trail.estimated_time() == pytest.approx(2.0)


# ============================================================
# WP-204 — Override + super()
# ============================================================

def test_guided_hike_extends_packing_list():
    trail = GuidedDayHike(
        name="Guided Hike",
        distance=Distance(8, "km"),
        elevation_gain_m=300,
        difficulty="moderate",
        guide_name="Sarah",
    )

    packing_list = trail.packing_list()

    assert "water" in packing_list
    assert "first aid kit" in packing_list
    assert "guide radio" in packing_list


def test_trail_run_has_different_packing_list():
    trail = TrailRun(
        name="Trail Run",
        distance=Distance(8, "km"),
        elevation_gain_m=300,
        difficulty="moderate",
    )

    packing_list = trail.packing_list()

    assert "running shoes" in packing_list
    assert "energy gel" in packing_list
    assert "tent" not in packing_list


# ============================================================
# WP-205 — Mixins
# ============================================================

def test_elevation_mixin():
    trail = RatedGuidedDayHike(
        name="Mountain Hike",
        distance=Distance(10, "km"),
        elevation_gain_m=500,
        difficulty="hard",
        guide_name="Alex",
        average_rating=4.5,
    )

    assert trail.average_grade_percent == pytest.approx(5.0)


def test_rating_mixin():
    trail = RatedGuidedDayHike(
        name="Mountain Hike",
        distance=Distance(10, "km"),
        elevation_gain_m=500,
        difficulty="hard",
        guide_name="Alex",
        average_rating=4.5,
    )

    assert trail.average_rating == 4.5


def test_mixin_mro():
    mro = RatedGuidedDayHike.__mro__

    assert mro[0] is RatedGuidedDayHike
    assert GuidedDayHike in mro
    assert DayHike in mro
    assert ElevationMixin in mro
    assert RatingMixin in mro
    assert Trail in mro


def test_mro_resolves_trail_note_to_elevation_mixin():
    trail = RatedGuidedDayHike(
        name="Mountain Hike",
        distance=Distance(10, "km"),
        elevation_gain_m=500,
        difficulty="hard",
        guide_name="Alex",
        average_rating=4.5,
    )

    # Both ElevationMixin and RatingMixin define trail_note().
    # ElevationMixin appears first in the MRO.
    assert trail.trail_note() == "Average grade: 5.0%"


# ============================================================
# WP-206 — Polymorphism
# ============================================================

def test_polymorphic_loop(capsys):
    trails = [
        DayHike(
            name="Hike",
            distance=Distance(10, "km"),
            elevation_gain_m=100,
            difficulty="moderate",
        ),
        BackpackingRoute(
            name="Backpacking",
            distance=Distance(10, "km"),
            elevation_gain_m=500,
            difficulty="moderate",
        ),
        TrailRun(
            name="Run",
            distance=Distance(10, "km"),
            elevation_gain_m=200,
            difficulty="moderate",
        ),
    ]

    print_estimated_times(trails)

    output = capsys.readouterr().out

    assert "DayHike" in output
    assert "BackpackingRoute" in output
    assert "TrailRun" in output


# ============================================================
# WP-206 — Duck typing
# ============================================================

def test_fake_trail_works_without_inheritance(capsys):
    trails = [
        DayHike(
            name="Hike",
            distance=Distance(10, "km"),
            elevation_gain_m=100,
            difficulty="moderate",
        ),
        FakeTrail(
            name="Fake",
            hours=1.25,
        ),
        TrailRun(
            name="Run",
            distance=Distance(10, "km"),
            elevation_gain_m=100,
            difficulty="moderate",
        ),
    ]

    print_estimated_times(trails)

    output = capsys.readouterr().out

    assert "DayHike" in output
    assert "FakeTrail" in output
    assert "TrailRun" in output
    assert "1.25 hours" in output