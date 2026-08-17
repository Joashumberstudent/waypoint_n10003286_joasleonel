from django.shortcuts import render


def home(request):
    
    context = {
        "greeting_name": "Waypoint Explorer",
    }
    return render(request, "home.html", context)


def report(request):
    
    if request.method == "POST":
        context = {
            "submitted": True,
            "name": request.POST.get("name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "trail": request.POST.get("trail", "").strip(),
            "note": request.POST.get("note", "").strip(),
        }
    else:
        context = {"submitted": False}
    return render(request, "report.html", context)


def search(request):
    
    query = request.GET.get("q", "")
    context = {"query": query}
    return render(request, "search.html", context)