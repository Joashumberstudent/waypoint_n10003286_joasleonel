from django.contrib import admin

from .models import Park, Trail


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "region",
    )

    search_fields = (
        "name",
        "region",
    )


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "park",
        "distance_km",
        "elevation_gain",
        "difficulty",
        "is_open",
        "added",
    )

    search_fields = (
        "name",
        "park__name",
        "difficulty",
    )

    list_filter = (
        "park",
        "difficulty",
        "is_open",
    )