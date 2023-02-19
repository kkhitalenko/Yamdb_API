from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    GetTokenView, SignupView, UserPersonalPageView, UserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/users/me/', UserPersonalPageView.as_view()),
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', GetTokenView.as_view()),
    path('v1/', include(router_v1.urls)),
]
