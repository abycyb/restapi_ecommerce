from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ecommerce import settings
from .views import *

urlpatterns = [
    path('registeruser/',UserCreationView.as_view(),name='register'),
    path('loginuser/',SigninView.as_view(),name='login'),
    path('create/', ProductListCreateView.as_view(), name='productmodel_create'),
    path('updatedelete/<int:pk>',ProductRetrieveUpdateDestroyView.as_view(),name='updatedelete'),
    path('addtocart/<int:id>/',AddToCartView.as_view(),name='addtocart'),
    path('addtocart/',AddToCartView.as_view(),name='addtocart'),
    path('address/',AddressView.as_view(),name='address'),
    path('addressdetail/<int:pk>/',AddressDetailView.as_view(),name='AddressDetail'),

    path('checkoutorder/',CheckoutOrder.as_view(),name='checkoutorder'),
    path('checkoutorder/<int:pk>/',CheckoutOrder.as_view(),name='checkoutorder')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
