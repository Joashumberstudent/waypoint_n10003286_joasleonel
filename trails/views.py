from django.shortcuts import render

from .models import Trail


def catalog(request):
    trails = Trail.objects.filter(
        is_open=True
    ).order_by(
        "distance_km"
    )

    return render(
        request,
        "catalog.html",
        {"trails": trails},
    )