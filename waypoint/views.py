from django.shortcuts import render

from trails.models import Trail
def home(request):
    context = {
        "greeting": "Welcome to Waypoint!"
    }

    return render(request, "home.html", context)


def report(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        trail = request.POST.get("trail", "")
        note = request.POST.get("note", "")

        context = {
            "name": name,
            "email": email,
            "trail": trail,
            "note": note,
            "submitted": True,
        }

        return render(request, "thank_you.html", context)

    return render(request, "report.html")


def search(request):
    query = request.GET.get("q", "")

    context = {
        "query": query,
    }

    return render(request, "search.html", context)


def catalog(request):
    trails = Trail.objects.filter(
        is_open=True
    ).order_by(
        "distance_km"
    )

    context = {
        "trails": trails,
    }

    return render(request, "catalog.html", context)