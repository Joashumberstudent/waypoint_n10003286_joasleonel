from django.urls import path

from . import views


urlpatterns = [
    path("", views.catalog, name="catalog"),
    path(
        "<int:trail_id>/",
        views.trail_detail,
        name="trail_detail",
    ),
]