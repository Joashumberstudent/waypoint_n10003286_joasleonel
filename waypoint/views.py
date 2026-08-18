from django.shortcuts import render


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
    trails = [
        {
            "name": "Mont Royal Loop",
            "distance": 5.2,
            "elevation": 210,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Lac Tremblant Trail",
            "distance": 8.7,
            "elevation": 340,
            "difficulty": "moderate",
            "is_open": True,
        },
        {
            "name": "Eagle Peak",
            "distance": 12.4,
            "elevation": 680,
            "difficulty": "hard",
            "is_open": False,
        },
        {
            "name": "Pine Ridge",
            "distance": 4.6,
            "elevation": 150,
            "difficulty": "easy",
            "is_open": True,
        },
        {
            "name": "Black Mountain",
            "distance": 15.8,
            "elevation": 920,
            "difficulty": "expert",
            "is_open": True,
        },
        {
            "name": "River Valley",
            "distance": 7.3,
            "elevation": 280,
            "difficulty": "moderate",
            "is_open": False,
        },
    ]

    context = {
        "trails": trails,
    }

    return render(request, "catalog.html", context)