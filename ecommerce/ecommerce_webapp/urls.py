from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ecommerce import settings
from .views import *

urlpatterns = [
    path('registeruser/',UserCreationView.as_view(),name='register'),
    path('loginuser/',SigninView.as_view(),name='login')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
