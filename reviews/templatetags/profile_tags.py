from django import template
from reviews.models import Review

register = template.Library()

@register.inclusion_tag('reviews/book_title_list.html')
def book_list(user):
    reviews = Review.objects.filter(creator=user)
    book_list = [review.book.title for review in reviews]
    return {'book_list': book_list}