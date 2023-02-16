from reviews.models import (
    Category, Genres, Title, Review
)
from rest_framework import serializers


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

    class Meta:
        fields = '__all__'
        model = Title

    def get_genre(self, obj):
        genre_query = Genres.objects.filter(genre=obj.id)
        serializer = GenresSerializer(genre_query, many=True)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Validates Review model."""

    class Meta:
        fields = '__all__'
        model = Review
