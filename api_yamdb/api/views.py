from api.serializers import (
    CategorySerializer, GenresSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)
from reviews.models import Title, Category, Genres, Review, Comment
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ReviewPermission


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
    permission_classes = (ReviewPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    """Review Comment."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)
    pagination_class = PageNumberPagination