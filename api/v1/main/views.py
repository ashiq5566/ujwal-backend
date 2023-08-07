
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
        number_of_semester = serializer.validated_data['number_of_semester']
        for i in range(1,number_of_semester+1):
            semester_name='Semester '+str(i)
            if not Semesters.objects.filter(semester=semester_name).exists():
                Semesters(semester=semester_name).save()

        program_instance = serializer.save()
        

        for i in range(number_of_semester,0,-1):
            semester_name='Semester '+str(i)
            semester_instance = Semesters.objects.get(semester=semester_name)
            Program_Semester(program=program_instance,semester=semester_instance).save()

        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Program created successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Program creation failed.",
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


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_program(request, program_id):
    try:
        program_instance = Programs.objects.get(id=program_id)
    except Programs.DoesNotExist:
        response_data = {
            "statusCode": 6002,
            "data": {
                "title": "Not Found",
                "message": "Program not found."
            }
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    serializer = ProgramPostSerializer(program_instance, data=request.data)

    if serializer.is_valid():
        program_instance = serializer.save()


        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Program updated successfully."
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Program update failed.",
            "errors": serializer.errors
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
