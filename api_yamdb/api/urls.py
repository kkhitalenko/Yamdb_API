from api.views import (
    TitleViewSet, GenresViewSet, ReviewViewSet, CategoryViewSet, CommentViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter


v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register(
    r'titles/(?P<id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
