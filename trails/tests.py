from django.test import TestCase
from django.urls import reverse

from .models import Park, Trail


class ParkModelTests(TestCase):

    def test_park_string(self):
        park = Park.objects.create(
            name="Gatineau Park",
            region="Outaouais",
        )

        self.assertEqual(
            str(park),
            "Gatineau Park (Outaouais)",
        )


class TrailRelationshipTests(TestCase):

    def setUp(self):
        self.park_one = Park.objects.create(
            name="Mont Royal Park",
            region="Montreal",
        )

        self.park_two = Park.objects.create(
            name="Gatineau Park",
            region="Outaouais",
        )

        self.trail_one = Trail.objects.create(
            name="Trail One",
            distance_km=5.00,
            elevation_gain=100,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
            park=self.park_one,
        )

        self.trail_two = Trail.objects.create(
            name="Trail Two",
            distance_km=8.00,
            elevation_gain=300,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
            park=self.park_two,
        )

        self.closed_trail = Trail.objects.create(
            name="Closed Trail",
            distance_km=2.00,
            elevation_gain=50,
            difficulty=Trail.Difficulty.EASY,
            is_open=False,
            park=self.park_one,
        )

    def test_trail_has_park(self):
        self.assertEqual(
            self.trail_one.park,
            self.park_one,
        )

    def test_park_has_related_trails(self):
        self.assertEqual(
            self.park_one.trails.count(),
            2,
        )

    def test_catalog_filters_by_park(self):
        response = self.client.get(
            reverse("catalog"),
            {"park": self.park_one.id},
        )

        self.assertContains(
            response,
            "Trail One",
        )

        self.assertNotContains(
            response,
            "Trail Two",
        )

    def test_closed_trails_are_not_shown(self):
        response = self.client.get(
            reverse("catalog"),
        )

        self.assertContains(
            response,
            "Trail One",
        )

        self.assertContains(
            response,
            "Trail Two",
        )

        self.assertNotContains(
            response,
            "Closed Trail",
        )

    def test_catalog_displays_park(self):
        response = self.client.get(
            reverse("catalog"),
        )

        self.assertContains(
            response,
            "Mont Royal Park",
        )

        self.assertContains(
            response,
            "Gatineau Park",
        )