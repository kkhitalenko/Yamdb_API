from django.contrib import admin
from reviews.models import (
    Category, Genres, Title, Review
)


admin.site.register(Category)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(Review)
