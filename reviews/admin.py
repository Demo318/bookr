from django.contrib import admin
from reviews.models import (
    Publisher,
    Contributor,
    Book,
    BookContributor,
    Review
)

class ContributorAdmin(admin.ModelAdmin):
    search_fields = ('last_names__startswith', 'first_names')
    list_display = ('last_names', 'first_names') #(initialed_name,)
    list_filter = ('last_names',)

class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = ('title','isbn__exact','publisher_name')
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13','has_isbn', 'get_publisher', 'publication_date')
    list_filter = ('publisher','publication_date')

    @admin.display(
            ordering='isbn',
            description='ISBN-13',
            empty_value='-/-'
    )
    def isbn13(self, obj):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(
            obj.isbn[0:3],
            obj.isbn[3:4],
            obj.isbn[4:6],
            obj.isbn[6:12],
            obj.isbn[12:13]
        )
    
    @admin.display(
        boolean=True,
        description='Has ISBN'
    )
    def has_isbn(self, obj):
        """ '9780316769174' => True """
        return bool(obj.isbn)
    
    def get_publisher(self, obj):
        return obj.publisher.name

class ReviewAdmin(admin.ModelAdmin):
    # exclude = ('date_edited',)
    # fields = ('content', 'rating', 'creator', 'book')
    fieldsets = (
        (None, {"fields": ("creator", "book")}),
        ("Review content", {"fields": ("content", "rating")}),
    )

admin.site.register(Publisher)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review, ReviewAdmin)

