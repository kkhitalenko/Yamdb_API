from reviews.models import (
    Title, GenreTitle, Review, User, Category, Genres
)
from rest_framework.validators import UniqueValidator
from rest_framework import serializers


class CategoryCmdSerializer(serializers.ModelSerializer):
    """Validates Category model."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Category.objects.all())
        ]
    )

    class Meta:
        fields = ['name', 'slug']
        model = Category
        lookup_field = 'slug'


class GenresCmdSerializer(serializers.ModelSerializer):
    """Validates Genres model."""

    slug = serializers.SlugField(
        max_length=50,
        validators=[
            UniqueValidator(queryset=Genres.objects.all())
        ]
    )

    class Meta:
        fields = ['name', 'slug']
        model = Genres
        lookup_field = 'slug'


class TitleCmdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'year', 'category']
        model = Title


class GenreTitleCmdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'title_id', 'genre_id']
        model = GenreTitle


class UserCmdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'username', 'email', 'role']
        model = User


class ReviewCmdSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source='title_id')

    class Meta:
        fields = ['id', 'title', 'text', 'author', 'score', 'pub_date']
        model = Review
