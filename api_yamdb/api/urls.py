from api.views import (
    TitleViewSet, GenresViewSet, ReviewViewSet, CategoryViewSet, CommentViewSet
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    GetTokenView, SignupView, UserPersonalPageView, UserViewSet
)


app_name = 'api'

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
v1_кщгеук.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/users/me/', UserPersonalPageView.as_view()),
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/', include(router_v1.urls)),
]
