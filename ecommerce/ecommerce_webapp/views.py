from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from rest_framework import status,generics,mixins,viewsets


# class UserCreationView(APIView):
#     def post(self,request):
#         serializer=UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"msg":serializer.data},status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

# class SigninView(APIView):
#     def post(self,request):
#         serializer=loginserializer(data=request.data)
#         if serializer.is_valid():
#             uname=serializer.validated_data.get("username")
#             password=serializer.validated_data.get("password")
#             user=authenticate(request,username=uname,password=password)
#             if user:
#                 login(request,user)
#                 return Response({"msg":"loggedd in successfully"})
#             else:
#                 return Response({"msg":"login failed"})        


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


# class SigninView(generics.CreateAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         return Response(serializer.validated_data)


class SigninView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)