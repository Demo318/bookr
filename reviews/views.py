from django.shortcuts import render

def index(request):
    name = "world"
    return render(request, "base.html", {"name": name})

def search(request):
    search_query = request.GET.get("search-query") or ""
    return render(request, "search_result.html", {"search_query": search_query})
