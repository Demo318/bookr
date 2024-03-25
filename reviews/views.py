from django.shortcuts import render
from django.http import HttpResponse
from .models import Book

def index(request):
    name = "world"
    return render(request, "base.html", {"name": name})

def search(request):
    search_query = request.GET.get("search-query") or ""
    return render(request, "search_result.html", {"search_query": search_query})

def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1><p>{Book.objects.count()} books and counting!</p></html>"
    return HttpResponse(message)
