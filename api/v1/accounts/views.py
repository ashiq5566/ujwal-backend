from django.contrib.auth.models import User

import requests
import json

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from .serializers import ( 
    LoginSerializer, 
)
from api.v1.accounts.functions import authenticate

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