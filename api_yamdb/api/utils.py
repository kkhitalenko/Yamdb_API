from api.permissions import IsAdminOrReadOnly
from rest_framework import filters, mixins
from rest_framework.viewsets import GenericViewSet


class CategoryGenresAbstractViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Abstract viewset with no PUT method."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
