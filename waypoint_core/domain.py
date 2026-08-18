from __future__ import annotations

from abc import ABC, abstractmethod
from math import isclose


# ============================================================
# WP-202 — Distance operators
# ============================================================

class Distance:
    CONVERSION = {
        ("km", "mi"): 0.621371,
        ("mi", "km"): 1.60934,
    }

    def __init__(self, magnitude, unit):
        if magnitude < 0:
            raise ValueError("Distance cannot be negative.")

        if unit not in ("km", "mi"):
            raise ValueError("Unit must be 'km' or 'mi'.")

        self._magnitude = magnitude
        self._unit = unit

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def unit(self):
        return self._unit

    def convert(self, target_unit):
        if target_unit not in ("km", "mi"):
            raise ValueError("Unit must be 'km' or 'mi'.")

        if target_unit == self._unit:
            return Distance(self._magnitude, self._unit)

        factor = self.CONVERSION[
            (self._unit, target_unit)
        ]

        return Distance(
            self._magnitude * factor,
            target_unit,
        )

    def __add__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented

        if self.unit != other.unit:
            other = other.convert(self.unit)

        return Distance(
            self.magnitude + other.magnitude,
            self.unit,
        )

    def __sub__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented

        if self.unit != other.unit:
            other = other.convert(self.unit)

        result = self.magnitude - other.magnitude

        if result < 0:
            raise ValueError(
                "Distance result cannot be negative."
            )

        return Distance(
            result,
            self.unit,
        )

    def __eq__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented

        other_converted = other.convert(self.unit)

        return abs(
            self.magnitude - other_converted.magnitude
        ) < 1e-9

    def __lt__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented

        other_converted = other.convert(self.unit)

        return (
            self.magnitude
            < other_converted.magnitude
        )

    def __gt__(self, other):
        if not isinstance(other, Distance):
            return NotImplemented

        other_converted = other.convert(self.unit)

        return (
            self.magnitude
            > other_converted.magnitude
        )

    def __str__(self):
        return f"{self.magnitude:g} {self.unit}"

    def __repr__(self):
        return (
            f"Distance({self.magnitude!r}, "
            f"{self.unit!r})"
        )
# ============================================================
# WP-201 — Abstract Trail
# ============================================================

class Trail(ABC):
    """
    Abstract base class for all trail types.

    Trail cannot be instantiated directly because every trail
    must provide its own estimated_time() and summary().
    """

    DEFAULT_UNIT = "km"

    ALLOWED_DIFFICULTIES = {
        "easy",
        "moderate",
        "hard",
    }

    def __init__(
        self,
        name: str,
        distance: Distance | float,
        elevation_gain_m: float,
        difficulty: str,
        trail_id=None,
    ):
        self._id = trail_id
        self._name = name
        self._elevation_gain_m = float(elevation_gain_m)

        if isinstance(distance, Distance):
            self._distance = distance
        else:
            self._distance = Distance(
                distance,
                self.DEFAULT_UNIT,
            )

        self._difficulty = None
        self.set_difficulty(difficulty)

    # --------------------------------------------------------
    # Properties
    # --------------------------------------------------------

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def distance(self) -> Distance:
        return self._distance

    @property
    def elevation_gain_m(self) -> float:
        return self._elevation_gain_m

    @property
    def difficulty(self) -> str:
        return self._difficulty

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    @staticmethod
    def validate_difficulty(difficulty: str) -> bool:
        return (
            isinstance(difficulty, str)
            and difficulty.lower()
            in Trail.ALLOWED_DIFFICULTIES
        )

    @staticmethod
    def validate_unit(unit: str) -> bool:
        return unit in Distance.VALID_UNITS

    def set_difficulty(self, difficulty: str) -> None:
        if not self.validate_difficulty(difficulty):
            raise ValueError(
                f"Invalid difficulty: {difficulty}"
            )

        self._difficulty = difficulty.lower()

    # --------------------------------------------------------
    # WP-103 — Default unit
    # --------------------------------------------------------

    @classmethod
    def set_default_unit(cls, unit: str) -> None:
        if not cls.validate_unit(unit):
            raise ValueError(
                "Default unit must be 'km' or 'mi'."
            )

        cls.DEFAULT_UNIT = unit

    # --------------------------------------------------------
    # WP-103 — API constructor
    # --------------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict) -> "Trail":
        """
        Concrete subclasses inherit this constructor.

        The dictionary can contain:

        "distance": 10

        or:

        "distance": {
            "magnitude": 10,
            "unit": "km"
        }
        """

        raw_distance = data["distance"]

        if isinstance(raw_distance, dict):
            distance = Distance(
                raw_distance["magnitude"],
                raw_distance["unit"],
            )
        else:
            distance = Distance(
                raw_distance,
                cls.DEFAULT_UNIT,
            )

        return cls(
            name=data["name"],
            distance=distance,
            elevation_gain_m=data["elevation_gain_m"],
            difficulty=data["difficulty"],
            trail_id=data.get("id"),
        )

    # --------------------------------------------------------
    # WP-104 — Entity equality
    # --------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Trail):
            return NotImplemented

        return self.id == other.id

    # --------------------------------------------------------
    # WP-201 — Abstract behavior
    # --------------------------------------------------------

    @abstractmethod
    def estimated_time(self) -> float:
        """
        Return estimated hiking/running time in hours.
        """
        pass

    @abstractmethod
    def summary(self) -> str:
        """
        Return a human-readable description.
        """
        pass


# ============================================================
# WP-201 — DayHike
# ============================================================

class DayHike(Trail):
    """
    A normal one-day hike.

    Pacing:
        Easy/moderate/hard hikes use different speeds.
    """

    PACE_KMH = {
        "easy": 4.5,
        "moderate": 4.0,
        "hard": 3.0,
    }

    def __init__(
        self,
        name: str,
        distance: Distance | float,
        elevation_gain_m: float,
        difficulty: str,
        trail_id=None,
    ):
        # WP-203 — super().__init__
        super().__init__(
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            trail_id=trail_id,
        )

    def estimated_time(self) -> float:
        speed = self.PACE_KMH[self.difficulty]

        distance_km = self.distance.convert("km").magnitude

        return distance_km / speed

    def summary(self) -> str:
        return (
            f"Day hike '{self.name}': "
            f"{self.distance}, "
            f"{self.difficulty} difficulty."
        )

    # WP-204 — type-specific behavior
    def packing_list(self) -> list[str]:
        return [
            "water",
            "snacks",
            "first aid kit",
            "map",
        ]


# ============================================================
# WP-201 — BackpackingRoute
# ============================================================

class BackpackingRoute(Trail):
    """
    Multi-day route.

    Backpacking is slower because of the backpack and
    multi-day equipment.
    """

    PACE_KMH = {
        "easy": 3.5,
        "moderate": 3.0,
        "hard": 2.5,
    }

    def __init__(
        self,
        name: str,
        distance: Distance | float,
        elevation_gain_m: float,
        difficulty: str,
        trail_id=None,
        nights: int = 1,
    ):
        # WP-203 — super().__init__
        super().__init__(
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            trail_id=trail_id,
        )

        if nights < 1:
            raise ValueError("A backpacking route needs at least 1 night.")

        self._nights = nights

    @property
    def nights(self) -> int:
        return self._nights

    def estimated_time(self) -> float:
        speed = self.PACE_KMH[self.difficulty]

        distance_km = self.distance.convert("km").magnitude

        return distance_km / speed

    def summary(self) -> str:
        return (
            f"Backpacking route '{self.name}': "
            f"{self.distance}, "
            f"{self.nights} night(s), "
            f"{self.difficulty} difficulty."
        )

    def packing_list(self) -> list[str]:
        return [
            "tent",
            "sleeping bag",
            "cooking equipment",
            "water",
            "food",
            "first aid kit",
        ]


# ============================================================
# WP-201 — TrailRun
# ============================================================

class TrailRun(Trail):
    """
    Trail running.

    Runners have a much faster pace than hikers.
    """

    PACE_KMH = {
        "easy": 8.0,
        "moderate": 7.0,
        "hard": 5.5,
    }

    def __init__(
        self,
        name: str,
        distance: Distance | float,
        elevation_gain_m: float,
        difficulty: str,
        trail_id=None,
    ):
        # WP-203 — super().__init__
        super().__init__(
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            trail_id=trail_id,
        )

    def estimated_time(self) -> float:
        speed = self.PACE_KMH[self.difficulty]

        distance_km = self.distance.convert("km").magnitude

        return distance_km / speed

    def summary(self) -> str:
        return (
            f"Trail run '{self.name}': "
            f"{self.distance}, "
            f"{self.difficulty} difficulty."
        )

    # WP-204 — override behavior
    def packing_list(self) -> list[str]:
        return [
            "running shoes",
            "water",
            "energy gel",
            "phone",
        ]


# ============================================================
# WP-203 — Further inheritance level
# ============================================================

class GuidedDayHike(DayHike):
    """
    A DayHike with a guide.

    Adds:
        guide_name
    """

    def __init__(
        self,
        name: str,
        distance: Distance | float,
        elevation_gain_m: float,
        difficulty: str,
        guide_name: str,
        trail_id=None,
    ):
        # WP-203 — super().__init__
        super().__init__(
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            trail_id=trail_id,
        )

        if not guide_name:
            raise ValueError("guide_name cannot be empty.")

        self._guide_name = guide_name

    @property
    def guide_name(self) -> str:
        return self._guide_name

    # WP-204 — extend parent method with super()
    def packing_list(self) -> list[str]:
        equipment = super().packing_list()

        equipment.append("guide radio")

        return equipment

    def summary(self) -> str:
        return (
            super().summary()
            + f" Guide: {self.guide_name}."
        )


# ============================================================
# WP-205 — Mixins
# ============================================================

class ElevationMixin:
    """
    Adds elevation/grade-related behavior.
    """

    @property
    def average_grade_percent(self) -> float:
        distance_m = self.distance.convert("km").magnitude * 1000

        if distance_m == 0:
            return 0.0

        return (
            self.elevation_gain_m
            / distance_m
            * 100
        )

    def trail_note(self) -> str:
        return (
            f"Average grade: "
            f"{self.average_grade_percent:.1f}%"
        )


class RatingMixin:
    """
    Adds a user rating to a trail.
    """

    def __init__(
        self,
        *args,
        average_rating: float = 0.0,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if not 0 <= average_rating <= 5:
            raise ValueError(
                "average_rating must be between 0 and 5."
            )

        self._average_rating = float(average_rating)

    @property
    def average_rating(self) -> float:
        return self._average_rating

    def trail_note(self) -> str:
        return (
            f"Average rating: "
            f"{self.average_rating:.1f}/5"
        )


# ============================================================
# WP-205 — Composed trail type
# ============================================================

class RatedGuidedDayHike(
    GuidedDayHike,
    ElevationMixin,
    RatingMixin,
):
    """
    A guided day hike with:

        - elevation information
        - user rating

    MRO demonstrates which implementation is selected
    when multiple classes provide trail_note().
    """

    def __init__(
        self,
        name: str,
        distance: Distance | float,
        elevation_gain_m: float,
        difficulty: str,
        guide_name: str,
        average_rating: float,
        trail_id=None,
    ):
        super().__init__(
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            guide_name=guide_name,
            trail_id=trail_id,
            average_rating=average_rating,
        )

    def summary(self) -> str:
        return (
            super().summary()
            + f" Rating: {self.average_rating:.1f}/5."
        )


# ============================================================
# WP-105 from Week 7 — Itinerary
# ============================================================

class Itinerary:
    """
    Ordered collection of Trail objects.

    The engine only requires the Trail interface.
    """

    def __init__(self, trails=None):
        self._trails = list(trails) if trails else []

    @property
    def trails(self) -> tuple:
        return tuple(self._trails)

    def add_trail(self, trail: Trail) -> None:
        if not isinstance(trail, Trail):
            raise TypeError(
                "Itinerary can only contain Trail objects."
            )

        self._trails.append(trail)

    def total_distance(
        self,
        unit: str | None = None,
    ) -> Distance:

        target_unit = unit or Trail.DEFAULT_UNIT

        total = Distance(0, target_unit)

        for trail in self._trails:
            total = total + trail.distance

        return total.convert(target_unit)

    def __len__(self):
        return len(self._trails)


# ============================================================
# WP-206 — Polymorphic engine
# ============================================================

def print_estimated_times(trails) -> None:
    """
    One loop works with every Trail subtype.

    No isinstance() checks are required.

    This is polymorphism:
        each object knows how to calculate its own time.
    """

    for trail in trails:
        print(
            f"{type(trail).__name__}: "
            f"{trail.estimated_time():.2f} hours"
        )


# ============================================================
# WP-206 — Duck-typed FakeTrail
# ============================================================

class FakeTrail:
    """
    Deliberately does NOT inherit from Trail.

    It still works with print_estimated_times() because
    the function only requires estimated_time().
    """

    def __init__(self, name: str, hours: float):
        self.name = name
        self.hours = hours

    def estimated_time(self) -> float:
        return self.hours

    def summary(self) -> str:
        return f"Fake trail: {self.name}"