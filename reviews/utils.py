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