from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):    
    ROLE_CHOICES = [
        ('OWNER', 'owner'),
        ('SUPERVISOR', 'supervisor'),
        ('CUSTOMER', 'customer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProfile')
    role = models.CharField(max_length = 30, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='userimg', blank=True, null=True, default=None)      

    def __str__(self):
        return self.user.get_full_name()
    

class ProductModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='productimg',null=True,blank=True, default=None)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

    def get_total_price(self):
        return self.item.price * self.quantity
    

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField()


class Order(models.Model):
    STATUS_TYPES = [
       ('PENDING', 'pending'), 
       ('ORDERED', 'orderd'),             
       ('SHIPPED', 'shipped'),
       ('ON THE WAY', 'on the way'),
       ('DELIVERD', 'deliverd'),
       ('CANCELLED', 'cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=30,choices=STATUS_TYPES)
    transaction_id = models.CharField(unique=True, max_length=100, null=True)
    totalprice = models.FloatField(blank=False)

    def __str__(self):
        return str(self.user)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    STATUS_TYPES = [
       ('PENDING', 'pending'), 
       ('ORDERED', 'orderd'),             
       ('SHIPPED', 'shipped'),
       ('ON THE WAY', 'on the way'),
       ('DELIVERD', 'deliverd'),
       ('CANCELLED', 'cancelled')
    ]
    product = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=30,choices=STATUS_TYPES)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(blank=False)

    def __str__(self):
        return str(self.product)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total