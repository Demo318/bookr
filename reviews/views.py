from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Book, Review
from .utils import average_rating, evaluate_reviews

def index(request):
    return render(request, 'base.html')

def book_search(request):
    search_text = request.get('search', '')
    return render(request, 'reviews/search-results.html', {'search_text': search_text})

def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews_stats = evaluate_reviews(book)
        book_list.append({
            'book': book,
            'book_rating': reviews_stats[0],
            'number_of_reviews': reviews_stats[1]
        })
    context = {'book_list': book_list}
    return render(request, 'reviews/book_list.html', context)

def book_detail(request, pk):
    book = Book.objects.get(pk=pk)

    reviews = Review.objects.filter(book=book)
    reviews_stats = evaluate_reviews(book, reviews)

    book.book_rating = reviews_stats[0]
    context = { 'book': book, 'reviews': reviews }
    return render(request, 'reviews/book_detail.html', context)


