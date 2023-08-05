
import requests
import json
from django.contrib.auth.models import Group

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from .serializers import *
from api.v1.accounts.functions import authenticate
from accounts.models import User
from main.models import *


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




@api_view(["POST"])
@permission_classes([AllowAny])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        first_name = serializer.data.get("first_name")
        last_name = serializer.data.get("last_name")
        username = serializer.data.get("username")
        password = serializer.data.get("password")
        email = serializer.data.get("email")
        role = serializer.data.get("role")
        department = serializer.data.get("department")
        
        if not User.objects.filter(username=username).exists():
            
            if True:
                if(department):
                    dep = Departments.objects.filter(id=department).latest("department_name")
                else:
                    dep=None
                user = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    role=role,
                    department=dep
                )
                user.set_password(password)
                user.save()

                #group creation after saving the user
                if role == 'Admin':
                    ru_group, created = Group.objects.get_or_create(
                        name="Admin"
                    )
                    ru_group.user_set.add(user)
                elif role == 'Placement_officer':
                    ru_group, created = Group.objects.get_or_create(
                        name="Placement_officer"
                    )
                    ru_group.user_set.add(user)
                elif role == 'HOD':
                    ru_group, created = Group.objects.get_or_create(
                        name="HOD"
                    )
                    ru_group.user_set.add(user)
                elif role == 'Staff_Coordinator':
                    ru_group, created = Group.objects.get_or_create(
                        name="Staff_Coordinator"
                    )
                    ru_group.user_set.add(user)
                else:
                    ru_group, created = Group.objects.get_or_create(
                        name="Student_cordinator"
                    )
                    ru_group.user_set.add(user)
                  
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "message":"registered SuccessFully"
                    }
                }
            else:
                 response_data = {
                    "statusCode":6001,
                    "data":{
                        "title":"SignUp Failed",
                        "message":"department not exists"
                    }
                }
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"SignUp Failed",
                "message":"username exists"
            }
        }
            
        return Response(response_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(['POST'])
@permission_classes([AllowAny])
def create_department(request):
    serializer = DepartmentPostSerializer(data=request.data)
    
    if serializer.is_valid():
        department_name = serializer.validated_data['department_name']
        
        if Departments.objects.filter(department_name=department_name).exists():
            response_data = {
                "statusCode": 6001,
                "data": {
                    "title": "Department Already Exists",
                    "message": f"Department with name {department_name} already exists."
                }
            }
            return Response(response_data, status=status.HTTP_409_CONFLICT)
        
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Department created successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Department creation failed.",
            "errors": serializer.errors
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def department_list(request):
    if Departments.objects.all():
        departments = Departments.objects.all()  
        serializer = DepartmentsGetSerializer(departments, many=True)
        
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


@api_view(['POST'])
@permission_classes([AllowAny])
def add_trainer(request):
    serializer = TrainerPostSerializer(data=request.data)
    
    if serializer.is_valid():
        
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Department created successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Department creation failed.",
            "errors": serializer.errors
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def trainers_list(request):
    if Trainers.objects.all():
        trainers = Trainers.objects.all()  
        serializer = TrainersGetSerializer(trainers, many=True)
        
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


@api_view(['POST'])
@permission_classes([AllowAny])
def add_recruiter(request):
    serializer = RecruiterPostSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Recruiter created successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Recruiter creation failed.",
            "errors": serializer.errors
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def recruiters_list(request):
    if Recruiters.objects.all():
        recruiter = Recruiters.objects.all()  
        serializer = RecruitersGetSerializer(recruiter, many=True)
        
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

@api_view(['POST'])
@permission_classes([AllowAny])
def add_program(request):
    serializer = ProgramPostSerializer(data=request.data)
    
    if serializer.is_valid():
        
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Department created successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Department creation failed.",
            "errors": serializer.errors
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([AllowAny])
def program_list(request):
    if Programs.objects.all():
        programs = Programs.objects.all()  
        serializer = ProgramsGetSerializer(programs, many=True)
        
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