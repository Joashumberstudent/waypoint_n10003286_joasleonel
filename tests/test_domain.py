import unittest

from waypoint_core.domain import Distance


class DistanceTests(unittest.TestCase):

    def test_negative_distance_is_rejected(self):
        with self.assertRaises(ValueError):
            Distance(-1, "km")

    def test_distance_addition(self):
        result = (
            Distance(3, "km")
            + Distance(2, "km")
        )

        self.assertEqual(
            result,
            Distance(5, "km"),
        )

    def test_mixed_units_are_auto_converted(self):
        result = (
            Distance(1, "km")
            + Distance(1, "mi")
        )

        self.assertAlmostEqual(
            result.magnitude,
            2.60934,
            places=4,
        )