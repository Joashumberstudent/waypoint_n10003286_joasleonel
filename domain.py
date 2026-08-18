from __future__ import annotations

from math import isclose
from typing import Any


class Distance:
    """
    Value object representing a distance.

    Supported units:
        - km
        - mi
    """

    _KM_TO_MI = 0.621371192237334
    _MI_TO_KM = 1.609344
    _VALID_UNITS = {"km", "mi"}

    def __init__(self, magnitude: float, unit: str):
        if magnitude < 0:
            raise ValueError("Distance cannot be negative.")

        if unit not in self._VALID_UNITS:
            raise ValueError("Unit must be 'km' or 'mi'.")

        self._magnitude = float(magnitude)
        self._unit = unit

    @property
    def magnitude(self) -> float:
        """Read-only distance magnitude."""
        return self._magnitude

    @property
    def unit(self) -> str:
        """Read-only distance unit."""
        return self._unit

    def convert(self, target_unit: str) -> "Distance":
        """
        Convert this distance to another supported unit.
        """
        if target_unit not in self._VALID_UNITS:
            raise ValueError("Unit must be 'km' or 'mi'.")

        if target_unit == self._unit:
            return Distance(self._magnitude, self._unit)

        if self._unit == "km" and target_unit == "mi":
            converted = self._magnitude * self._KM_TO_MI
        else:
            converted = self._magnitude * self._MI_TO_KM

        return Distance(converted, target_unit)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Distance):
            return NotImplemented

        return (
            self.unit == other.unit
            and isclose(
                self.magnitude,
                other.magnitude,
                rel_tol=1e-9,
                abs_tol=1e-9,
            )
        )

    def __repr__(self) -> str:
        return f"Distance({self.magnitude}, '{self.unit}')"


class Trail:
    """
    Domain entity representing a hiking trail.
    """

    DEFAULT_UNIT = "km"

    _ALLOWED_DIFFICULTIES = {
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
        trail_id: Any = None,
    ):
        self._id = trail_id
        self._name = name
        self._elevation_gain_m = float(elevation_gain_m)
        self._difficulty = None

        # Distance can either be a Distance object or a numeric value.
        if isinstance(distance, Distance):
            self._distance = distance
        else:
            self._distance = Distance(
                distance,
                self.DEFAULT_UNIT,
            )

        self.set_difficulty(difficulty)

    @property
    def id(self) -> Any:
        return self._id

    @property
    def name(self) -> str:
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

    def set_difficulty(self, difficulty: str) -> None:
        """
        Change the trail difficulty after validating it.
        """
        if not self.validate_difficulty(difficulty):
            raise ValueError(
                f"Invalid difficulty '{difficulty}'. "
                f"Allowed values: {sorted(self._ALLOWED_DIFFICULTIES)}"
            )

        self._difficulty = difficulty

    @classmethod
    def set_default_unit(cls, unit: str) -> None:
        """
        Change the platform's default unit.

        This affects newly created trails that receive a numeric
        distance. Existing Trail objects are not modified.
        """
        if not cls.validate_unit(unit):
            raise ValueError("Default unit must be 'km' or 'mi'.")

        cls.DEFAULT_UNIT = unit

    @classmethod
    def from_dict(cls, data: dict) -> "Trail":
        """
        Build a Trail from an API-shaped dictionary.

        Expected examples:

        {
            "id": 101,
            "name": "Mont Royal",
            "distance": 5.5,
            "elevation_gain_m": 150,
            "difficulty": "moderate"
        }

        Or:

        {
            "id": 101,
            "name": "Mont Royal",
            "distance": {
                "magnitude": 5.5,
                "unit": "km"
            },
            "elevation_gain_m": 150,
            "difficulty": "moderate"
        }
        """

        trail_id = data.get("id")

        name = data["name"]
        elevation_gain_m = data["elevation_gain_m"]
        difficulty = data["difficulty"]

        raw_distance = data["distance"]

        if isinstance(raw_distance, dict):
            magnitude = raw_distance["magnitude"]
            unit = raw_distance["unit"]
            distance = Distance(magnitude, unit)
        else:
            distance = Distance(
                raw_distance,
                cls.DEFAULT_UNIT,
            )

        return cls(
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            trail_id=trail_id,
        )

    @staticmethod
    def validate_difficulty(difficulty: str) -> bool:
        """
        Validate a difficulty value.
        """
        return (
            isinstance(difficulty, str)
            and difficulty.lower() in Trail._ALLOWED_DIFFICULTIES
        )

    @staticmethod
    def validate_unit(unit: str) -> bool:
        """
        Validate a distance unit.
        """
        return unit in Distance._VALID_UNITS

    def __eq__(self, other: object) -> bool:
        """
        Two trails are equal when they have the same ID.
        """
        if not isinstance(other, Trail):
            return NotImplemented

        return self.id == other.id

    def __repr__(self) -> str:
        return (
            f"Trail("
            f"id={self.id!r}, "
            f"name={self.name!r}, "
            f"distance={self.distance!r}, "
            f"elevation_gain_m={self.elevation_gain_m}, "
            f"difficulty={self.difficulty!r}"
            f")"
        )


class Itinerary:
    """
    An ordered collection of trails.
    """

    def __init__(self, trails: list[Trail] | None = None):
        # Make a copy so different itineraries never share the same list.
        self._trails = list(trails) if trails is not None else []

    @property
    def trails(self) -> tuple[Trail, ...]:
        """
        Read-only view of the itinerary's trails.
        """
        return tuple(self._trails)

    def add_trail(self, trail: Trail) -> None:
        """
        Add a trail to the end of the itinerary.
        """
        if not isinstance(trail, Trail):
            raise TypeError("Itinerary can only contain Trail objects.")

        self._trails.append(trail)

    def total_distance(self, unit: str | None = None) -> Distance:
        """
        Calculate the total distance.

        If no unit is provided, Trail.DEFAULT_UNIT is used.
        """
        target_unit = unit or Trail.DEFAULT_UNIT

        if not Distance._VALID_UNITS.__contains__(target_unit):
            raise ValueError("Unit must be 'km' or 'mi'.")

        total = 0.0

        for trail in self._trails:
            total += trail.distance.convert(target_unit).magnitude

        return Distance(total, target_unit)

    def __len__(self) -> int:
        return len(self._trails)

    def __repr__(self) -> str:
        return f"Itinerary(trails={self._trails!r})"