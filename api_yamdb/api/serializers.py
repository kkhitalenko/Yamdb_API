from django.db.models import Avg
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import (
    Category, Genres, Title, Review, Comment
)


class CategorySerializer(serializers.ModelSerializer):
    """Validates Category model."""

    class Meta:
        fields = ['name', 'slug']
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    """Validates Genres model."""

    class Meta:
        fields = ['name', 'slug']
        model = Genres


class TitleSerializer(serializers.ModelSerializer):
    """Validates Title model."""

    category = CategorySerializer(read_only=True)
    genre = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_genre(self, obj):
        genre_query = Genres.objects.filter(genre=obj.id)
        serializer = GenresSerializer(genre_query, many=True)
        return serializer.data

    def get_title_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        if reviews.exists():
            rating = reviews.aggregate(Avg('score'))['score__avg']
            return int(round(rating))
        else:
            return 1


class ReviewSerializer(serializers.ModelSerializer):
    """Validates Review model."""

    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Пользователь может оставить только один отзыв!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Validates Comment model."""

    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comment
