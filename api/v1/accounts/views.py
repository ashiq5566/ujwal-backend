
import requests
import json

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from .serializers import ( 
    LoginSerializer,
    UserSerializer
)
from api.v1.accounts.functions import authenticate
from accounts.models import User

@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    serialized_data = LoginSerializer(data=request.data)
    if serialized_data.is_valid():
        username = request.data['username']
        password = request.data['password']
        
        response_data = authenticate(username,password,request)
    else:
        response_data = {
            "statusCode":6001,
            "data": {
                "title":"failed",
                "massage":"invalid credentials"
            }
        }            

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def user_list(request):
    if User.objects.all():
        user = User.objects.all()  
        serializer = UserSerializer(user, many=True)
        
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":serializer.data
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def user_details(request, pk):
    if User.objects.get(id=pk):
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        print("hwlel",pk)
        
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":serializer.data
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)