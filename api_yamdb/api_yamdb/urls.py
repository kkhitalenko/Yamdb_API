from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import path
>>>>>>> cf33cd88c55eb545e64c495d4fe0aff3c0121c91
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
