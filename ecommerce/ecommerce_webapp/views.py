from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from rest_framework import status,generics,mixins,viewsets
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    

class Usereditdelete(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]



    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def put(self, request):
    #     # user = self.get_object()
    #     user = request.user
        
    #     serializer = self.serializer_class(user, data=request.data)

    #     serializer.is_valid(raise_exception=True)        
    #     validated_data = serializer.validated_data
    #     user_profile = UserProfile.objects.filter(user=user)
    #     # .update(image=validated_data['image'])
    #     user_profile.update(image=validated_data.get('image'))
    #     # user_profile.save()
    #     if 'password' in validated_data:
    #         user.set_password(validated_data['password'])
    #         user.save()
    #         return Response(serializer.data)
        

# class UserUpdateDelete(APIView):
#     permission_classes = [IsAuthenticated]

#     # def get(self,request):
#     #     profile = User.objects.get(id=request.user.id)
#     #     print(profile.username,profile.email)
#     #     serializer = UserUpdateDeleteserializer(profile)
#     #     return Response(serializer.data)
#     def put(self, request):
#         user = request.user

#         serializer = UserUpdateDeleteserializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class SigninView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request_id=request.user.id
        user=UserProfile.objects.get(user_id=request_id)        
        if user.role == 'SUPERVISOR':
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"User role is Not authorized for this action"})
        

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, id, *args, **kwargs):
        product_model = ProductModel.objects.get(id=id)
        cart_item = CartItem.objects.filter(user=request.user,item=product_model)        
        if cart_item:
            return Response({"product already in cart"})
        else:
            cart = CartItem(
                user = request.user,
                item = product_model
            )
            cart.save()
        serializer = CartItemSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id, *args, **kwargs):
        cart_item = CartItem.objects.get(item__id=id)
        quantity = request.data.get('quantity')
        if quantity:
            cart_item.quantity = quantity
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    
    def delete(self,request,id,*args,**kwargs):
        cart_item = get_object_or_404(CartItem, item_id=id, user=request.user)
        cart_item.delete()
        return Response({"item deleted"})


class AddressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):                                        # getting all addresses instances
        address = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(address ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,*args,**kwargs):      
        data = Address.objects.all().filter(user=request.user)
        if (len(data)) < 3:
            address = Address(
                user=request.user,
                address = request.POST.get('address'),
                state = request.POST.get('state'),
                pincode = request.POST.get('pincode'),
            )
            address.save()
            serializer = AddressSerializer(address)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:    
            return Response({'Edit any one of the existing addresses'})           


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):                                         # getting single address instance
        address = Address.objects.get(user=request.user,id=pk)
        serializer = AddressSerializer(instance=address)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        addr = Address.objects.get(user=request.user,id=pk)
        serializer = AddressSerializer(instance=addr, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        addr = Address.objects.get(user=request.user,id=pk)
        addr.delete()
        return Response({"Address Deleted"})


class CheckoutOrder(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(cart ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):

        cart = CartItem.objects.filter(user=request.user)
        address_ = request.POST.get('address')
        addres_data = get_object_or_404(Address,user=request.user,id=address_)
        # or use this method # add = Address.objects.get(user=request.user,id=address_)       
        
        if cart:
            sum_total_price = 0
            for i in cart:
                sum_total_price += i.quantity * i.item.price
            
            order = Order(
                user = request.user,
                address = addres_data,
                totalprice = sum_total_price,
                status = 'ORDERED'
            )
            order.save()

            order_items = []
            for i in cart:
                order_item = OrderItem(
                    product = i.item.name,
                    order = order,
                    status = 'ORDERED',
                    quantity = i.quantity,
                    price = i.item.price * i.quantity
                )
                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)
            CartItem.objects.all().filter(user = request.user).delete()
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        return Response({"No items in the cart"})
    
    def put(self,request,pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'CANCELLED'
        order.save()
        item = OrderItem.objects.all().filter(order=order)
        for i in item:
            i.status = 'CANCELLED'
            i.save()
        return Response({"Order cancelled"})
    

class CancelOrderItem(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        cart = OrderItem.objects.filter(order__user=request.user)
        print(cart)
        serializer = OrderItemSerializer(cart ,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,id):
        cart = OrderItem.objects.get(order__user=request.user,id=id)
        if cart.status != "CANCELLED":
            cart.status = 'CANCELLED'
            cart.save()
            check_status = OrderItem.objects.all().filter(order__id=cart.order.id)
            print(check_status)
            # for i in check_status:
            #     if i.status == 'CANCELLED':
            #         print(i.status)
            if all(i.status == 'CANCELLED' for i in check_status) == True:
                order = get_object_or_404(Order, id=cart.order.id)
                order.status = 'CANCELLED'
                order.save()
            return Response({"Order item Cancelled"},status=status.HTTP_200_OK)
        return Response({"Order already Cancelled"},status=status.HTTP_200_OK)
