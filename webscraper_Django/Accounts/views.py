from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth import authenticate,login
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.models import User
# from 
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    print(request.data)
    try:
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"message": "Email and password are required"}, status=400)
        
        user = authenticate(request,username=email,password=password)
        if user is None:
            return Response({"message": "Invalid email or password"}, status=400)
        print(user)
        login(request,user)
        return Response({"message":"Sucessfully Logined!"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"message": "User login failed!", "error": str(e)}, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
    try:
        data = request.data
        print(data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User signed up successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            errors = serializer.errors.copy()
            print("errors :---")
            print(errors)
            return Response(
                {"message": "User signup failed!", "errors": errors},
                status=400
            )
    except Exception as e:
        print("E :---")
        print(e)
        return Response({"message": "User signup failed!", "error": str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_loggedin(request):
    print("Request User :---")
    print(request)
    print(request.user)
    if request.user.is_authenticated:
        return Response({"is_loggedin": True, "username": request.user.username}, status=200)
    else:
        return Response({"is_loggedin": False}, status=200)
 
@api_view(['GET'])
@permission_classes([IsAuthenticated])   
def profile(req):
    try:
        user = req.user
        user_data = {
            "username": user.username,
            "email": user.email,
        }
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        print(user_data)
        return Response(user_data, status=200)
    except Exception as e:
        return Response({"message": "Profile retrieval failed!", "error": str(e)}, status=400)




