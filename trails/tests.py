from django.test import TestCase
from django.urls import reverse

from .models import Park, Trail


class TrailQueryTests(TestCase):

    def setUp(self):
        self.park = Park.objects.create(
            name="Gatineau Park",
            region="Outaouais",
        )

        self.open_trail = Trail.objects.create(
            name="Open Trail",
            distance_km=5.50,
            elevation_gain=200,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
            park=self.park,
        )

        self.closed_trail = Trail.objects.create(
            name="Closed Trail",
            distance_km=8.00,
            elevation_gain=400,
            difficulty=Trail.Difficulty.HARD,
            is_open=False,
            park=self.park,
        )

    def test_catalog_only_shows_open_trails(self):
        response = self.client.get(
            reverse("catalog")
        )

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            "Open Trail",
        )

        self.assertNotContains(
            response,
            "Closed Trail",
        )


class TrailDetailTests(TestCase):

    def test_missing_trail_returns_404(self):
        response = self.client.get(
            "/trails/99999/"
        )

        self.assertEqual(
            response.status_code,
            404,
        )