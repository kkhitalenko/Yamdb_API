from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import path
>>>>>>> 4c6930b (Revert "Feature/category,genre,review")
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
