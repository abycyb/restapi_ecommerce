from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'role', 'image')

# class UserSerializer(serializers.ModelSerializer):
#     UserProfile = UserProfileSerializer()

#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password', 'UserProfile')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         profile_data = validated_data.pop('UserProfile')
#         password = validated_data.pop('password')
#         user = User.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()
#         UserProfile.objects.create(user=user, **profile_data)
#         return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)    
    image = serializers.ImageField(default=None)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'image']

    def create(self, validated_data):
        user_image = validated_data.pop('image')
        user = User.objects.create_user(**validated_data)        
        user_profile = UserProfile(user=user, role='CUSTOMER',image=user_image)
        user_profile.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields = ('id', 'name', 'description', 'image', 'price')


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'price', 'status')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ('id', 'user', 'date_ordered', 'complete', 'address', 'status', 'totalprice', 'order_items')