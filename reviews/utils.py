from django.db.models import Q
import datetime
from django.db.models import Count
from reviews.models import Review, Book

def get_books_read(username):
    """Get the list of books read by a user.
        :param: str username for whom the
            book records should be returned
        :return: list of dict of books read
            and date of posting the review
        """
    books = Review.objects.filter(creator__username__contains=username).all()
    # This makes sense because you can only have one review per book per user.
    return [{'title': book_read.book.title, 'completed_on': book_read.date_created} for book_read in books]

def get_books_read_by_month(username):
    """Get the books read by the user on per month
        basis.
    :param: str The username for which the books needs
        to be returned
    :return: dict of month wise books read
    """
    current_year = datetime.datetime.now().year
    books = Review.objects.filter(
        creator__username__contains=username,
        date_created__year=current_year).values('date_created__month').annotate(book_count=Count('book__title'))
    return books

def average_rating(rating_list):
    """Provides average rating of book reviews."""
    if not rating_list:
        return 0
    return round(sum(rating_list) / len(rating_list))

def evaluate_reviews(book, reviews=None):
    """Retrieves reviews associated with book."""
    if not reviews:
        reviews = book.review_set.all()
    if reviews:
        return (
            average_rating([review.rating for review in reviews]),
            len(reviews)
        )
    return ( None, 0 )

def query_book_contributor_by_names(name):
    print('names?')
    return Q(contributor__first_names__icontains=name) | Q(contributor__last_names__icontains=name)

def query_book_contributor_by_title(title):
    return Q(book__title__icontains=title)

def retrieve_book_contributors(query, criteria):
    """Queries DB for BookContributor objects based on criteria."""
    if criteria == 'title':
        return query_book_contributor_by_title(query)
    elif criteria == 'contributor':
        print('querycontr')
        return query_book_contributor_by_names(query)
    else:
        return query_book_contributor_by_title(query) | query_book_contributor_by_names(query)
