from django.test import TestCase
from django.urls import reverse


class Week11TemplateTests(TestCase):

    def test_home_uses_base_template(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "home.html")

    def test_search_uses_base_template(self):
        response = self.client.get(reverse("search"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "search.html")

    def test_report_uses_base_template(self):
        response = self.client.get(reverse("report"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "report.html")

    def test_catalog_exists(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "catalog.html")

    def test_catalog_contains_six_trails(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "Mont Royal Loop")
        self.assertContains(response, "Lac Tremblant Trail")
        self.assertContains(response, "Eagle Peak")
        self.assertContains(response, "Pine Ridge")
        self.assertContains(response, "Black Mountain")
        self.assertContains(response, "River Valley")

    def test_catalog_shows_closed_badge(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "CLOSED")

    def test_expert_trail_shows_hard_badge(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "HARD")

    def test_distance_is_formatted(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "5.2 km")
        self.assertContains(response, "8.7 km")