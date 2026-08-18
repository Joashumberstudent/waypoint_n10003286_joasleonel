from django.shortcuts import get_object_or_404, render

from .models import Park, Trail


def catalog(request):
    park_id = request.GET.get("park")

    trails = (
        Trail.objects
        .filter(is_open=True)
        .select_related("park")
        .order_by("distance_km")
    )

    selected_park = None

    if park_id:
        trails = trails.filter(
            park_id=park_id
        )

        selected_park = Park.objects.filter(
            id=park_id
        ).first()

    parks = Park.objects.all().order_by("name")

    context = {
        "trails": trails,
        "parks": parks,
        "selected_park": selected_park,
    }

    return render(
        request,
        "catalog.html",
        context,
    )


def trail_detail(request, trail_id):
    trail = get_object_or_404(
        Trail.objects.select_related("park"),
        id=trail_id,
        is_open=True,
    )

    return render(
        request,
        "trail_detail.html",
        {
            "trail": trail,
        },
    )