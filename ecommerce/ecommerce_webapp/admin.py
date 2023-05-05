from django.contrib import admin
from .models import *

admin.site.register(UserProfile)
admin.site.register(ProductModel)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)