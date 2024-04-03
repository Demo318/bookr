from io import BytesIO
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.core.files.images import ImageFile
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from .models import Book, Review, Contributor, BookContributor, Publisher
from .utils import average_rating, evaluate_reviews, retrieve_book_contributors
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm

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

    if request.user.is_authenticated:
        max_viewed_books_length=10
        viewed_books = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session['viewed_books'] = viewed_books

    reviews = Review.objects.filter(book=book)
    reviews_stats = evaluate_reviews(book, reviews)

    book.book_rating = reviews_stats[0]
    context = { 'book': book, 'reviews': reviews }
    return render(request, 'reviews/book_detail.html', context)

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
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

@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is not None:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            updated_review.book = book
            updated_review.date_edited = timezone.now()
            updated_review.save()
            if review is None:
                messages.success(
                    request,
                    "Review for \"{}\" has been created.".format(book.title)
                )
            else:
                messages.success(
                    request,
                    "Reivew for \"{}\" has been updated.".format(book.title)
                )
            return redirect('book_detail', book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(
        request,
        'reviews/instance_form.html',
        {
            'form': form,
            'instance': review,
            'model_type': 'Review',
            'related_instance': book,
            'related_model_type': 'Book',
        }
    )

@login_required
def book_media(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    form = BookMediaForm(data=request.POST, files=request.FILES, instance=instance)
    if request.method == 'POST':
        
        if form.is_valid():
            instance = form.save(False)
            if request.FILES.get('cover'):
                uploaded_image = form.cleaned_data['cover']
                image = Image.open(uploaded_image)
                image.thumbnail((300,300))
                image_data = BytesIO()
                image.save(fp=image_data, format=image.format)
                image_file = ImageFile(image_data)
                instance.cover.save(uploaded_image.name, image_file)
            instance.save()
            messages.success(
                request,
                "{} was updated.".format(instance.title)
            )
            return redirect('book_detail', instance.pk)
    return render(
        request,
        'reviews/instance_form.html',
        {
            'form': form,
            'instance': instance,
            'model_type': 'Book',
            'is_file_upload': True
        }
    )