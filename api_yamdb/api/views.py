from django.shortcuts import get_object_or_404
from api.serializers import (
    CategorySerializer, GenresSerializer, TitleSerializer,
    ReviewSerializer, CommentSerializer
)
from reviews.models import Title, Category, Genres, Review
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ReviewCommentPermission


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


class ReviewViewSet(viewsets.ModelViewSet):
    """Review ViewSet."""

    serializer_class = ReviewSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Review Comment."""

    serializer_class = CommentSerializer
    permission_classes = (ReviewCommentPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
