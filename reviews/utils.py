from django.db.models import Q

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
