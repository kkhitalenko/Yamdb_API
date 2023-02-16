from api.serializers import (
    CategorySerializer, GenresSerializer, TitleSerializer,
    ReviewSerializer
)
from reviews.models import Title, Category, Genres, Review
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class TitleViewSet(ModelViewSet):
    """Title ViewSet."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year',)


class CategoryViewSet(ModelViewSet):
    """Category ViewSet."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(ModelViewSet):
    """Genres ViewSet."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class ReviewViewSet(ModelViewSet):
    """Review ViewSet."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
