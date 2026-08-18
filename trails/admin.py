from django.contrib import admin

from .models import Trail


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "distance_km",
        "elevation_gain",
        "difficulty",
        "is_open",
        "added",
    )

    search_fields = (
        "name",
        "difficulty",
    )