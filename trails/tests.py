from django.test import TestCase
from django.urls import reverse

from .models import Trail


class TrailModelTests(TestCase):

    def test_trail_string(self):
        trail = Trail.objects.create(
            name="Mont Royal Loop",
            distance_km=5.20,
            elevation_gain=210,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )

        self.assertEqual(str(trail), "Mont Royal Loop")


class TrailCatalogTests(TestCase):

    def setUp(self):
        Trail.objects.create(
            name="Short Open Trail",
            distance_km=3.00,
            elevation_gain=100,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )

        Trail.objects.create(
            name="Long Open Trail",
            distance_km=10.00,
            elevation_gain=500,
            difficulty=Trail.Difficulty.HARD,
            is_open=True,
        )

        Trail.objects.create(
            name="Closed Trail",
            distance_km=1.00,
            elevation_gain=50,
            difficulty=Trail.Difficulty.EASY,
            is_open=False,
        )

    def test_catalog_only_shows_open_trails(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "Short Open Trail")
        self.assertContains(response, "Long Open Trail")
        self.assertNotContains(response, "Closed Trail")

    def test_catalog_orders_by_distance(self):
        response = self.client.get(reverse("catalog"))

        trails = response.context["trails"]

        self.assertEqual(
            list(trails.values_list("name", flat=True)),
            [
                "Short Open Trail",
                "Long Open Trail",
            ],
        )