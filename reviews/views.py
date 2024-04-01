from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import Book, Review, Contributor, BookContributor, Publisher
from .utils import average_rating, evaluate_reviews, retrieve_book_contributors
from .forms import SearchForm, PublisherForm

def index(request):
    return render(request, 'base.html')

def book_search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        print(f"Search in: {type(form.cleaned_data["search_in"])}")
        book_contributors = BookContributor.objects.filter(
            retrieve_book_contributors(
                form.cleaned_data["search"],
                criteria=form.cleaned_data["search_in"])
        )
        print(book_contributors)
        books = {}
        for bc in book_contributors:
            bc.contributor.role = bc.role
            bc.contributor.name = bc.contributor.initialed_name()
            if bc.book not in books.keys():
                books[bc.book] = [bc.contributor]
            else:
                books[bc.book].append(bc.contributor)
    search_text = request.GET.get('search', '')
    return render(
        request,
        'reviews/search_result.html',
        context = {
            'search_text': search_text,
            'form': form,
            'books': books
        }
    )

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

def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(
                    request,
                    "Publisher \"{}\" was created.".format(updated_publisher)
                )
            else:
                messages.success(
                    request,
                    "Publisher \"{}\" was updated.".format(updated_publisher)
                )
            return redirect('publisher_edit', updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    return render(
        request,
        'reviews/instance_form.html',
        {'form': form, 'instance': publisher, 'model_type': 'Publisher'}
    )
