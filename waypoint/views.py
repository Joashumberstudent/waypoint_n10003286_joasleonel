from django.shortcuts import render


# ============================================================
# WP-402 — Home
# ============================================================

def home(request):
    context = {
        "greeting": "Welcome to Waypoint!",
    }

    return render(
        request,
        "home.html",
        context,
    )


# ============================================================
# WP-403 — Trail report
# ============================================================

def report(request):

    if request.method == "GET":
        return render(
            request,
            "report.html",
        )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        trail = request.POST.get("trail", "").strip()
        note = request.POST.get("note", "").strip()

        context = {
            "name": name,
            "email": email,
            "trail": trail,
            "note": note,
        }

        return render(
            request,
            "thank_you.html",
            context,
        )

    return render(
        request,
        "report.html",
    )


# ============================================================
# WP-404 — Search
# ============================================================

def search(request):
    query = request.GET.get("q", "").strip()

    context = {
        "query": query,
    }

    return render(
        request,
        "search.html",
        context,
    )