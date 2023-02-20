from django.contrib import admin
from reviews.models import (
    Category, Genres, Title, Review, GenreTitle
)


class GTInline(admin.TabularInline):
    model = GenreTitle
    extra = 1


class GenreAdmin(admin.ModelAdmin):
    inlines = (GTInline,)


class TitileAdmin(admin.ModelAdmin):
    inlines = (GTInline,)


admin.site.register(Category)
admin.site.register(Genres, GenreAdmin)
admin.site.register(Title, TitileAdmin)
admin.site.register(Review)
