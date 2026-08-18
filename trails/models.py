from django.db import models


class Park(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.region})"


class Trail(models.Model):
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MODERATE = "moderate", "Moderate"
        HARD = "hard", "Hard"
        EXPERT = "expert", "Expert"

    name = models.CharField(max_length=200)

    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    elevation_gain = models.IntegerField()

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MODERATE,
    )

    is_open = models.BooleanField(default=True)

    added = models.DateTimeField(auto_now_add=True)

    park = models.ForeignKey(
        Park,
        on_delete=models.PROTECT,
        related_name="trails",
        null=True,
    )

    @property
    def distance(self):
        return self.distance_km

    @property
    def elevation(self):
        return self.elevation_gain

    def __str__(self):
        return self.name