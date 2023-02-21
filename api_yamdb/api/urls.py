from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet, CommentViewSet, GenresViewSet,
    GetTokenView, ReviewViewSet, SignupView, TitleViewSet,
    UserPersonalPageView, UserViewSet
)

v1_router = DefaultRouter()
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', UserPersonalPageView.as_view()),
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/', include(v1_router.urls)),
]
