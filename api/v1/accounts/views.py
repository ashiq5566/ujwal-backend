
import requests
import json
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from datetime import timedelta, datetime

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
        
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(password):
                headers = {
                    "Content-Type" : "application/json"
                }
                protocol = "http://"
                if request.is_secure():
                    protocol = "https://"

                web_host = request.get_host()
                request_url = protocol + web_host + "/api/v1/accounts/token/"
                data={
                    'grant_type': 'password',
                    'username': username,
                    'password': password,
                }
                response = requests.post(request_url, headers=headers, data=json.dumps(data))
                if(user.is_active):
                    response_data = {
                        'statusCode' : 6000,
                        'data' : {
                            'title': 'Success',
                                    "data":{
                                "id":user.id,
                                "username":user.username,
                                "role":user.role,
                                "email":user.email,

                            },
                            'response' : response.json(),
                        }
                    }
                    if user.department:
                        response_data['data']['data']['department'] = user.department.id
                    if user.role == 'student' and Student.objects.filter(admission_number=user.username).exists():
                        student = Student.objects.get(admission_number=user.username)
                        response_data['data']['data']['student']=student.id
                        response_data['data']['data']['program']=student.program.program_name
                        response_data['data']['data']['name']=student.first_name + ' ' + student.last_name 
                else:
                    response_data = {
                        "statusCode": 6001,
                        "data":{
                            "title": "Validation Error",
                            "message": "Invalied Credentials" #User inactive
                        }
                    }
            else:
                response_data = {
                    'statusCode' : 6001,
                    'data' : {
                        'title': 'failed',
                        'message' : "Incorrect password"
                    }
                }
        else:
            response_data = {
                'statusCode' : 6001,
                'data' : {
                    'title': 'failed',
                    'message' : "Invalied Credentials" #User not exists
                }
            }
    else:
        response_data = {
            "statusCode": 6001,
            "data":{
                "title": "Validation Error",
                "message": serialized_data._errors
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
    users = User.objects.filter(user_active=True).exclude(role__in=['student', 'Admin'])

    user_data = []

    for user in users:
        user_info = UserSerializer(user).data

        # Check if the user has a department associated with them
        if user.department:
            department_info = DepartmentsGetSerializer(user.department).data
            user_info['department'] = department_info

        user_data.append(user_info)

    if user_data:
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "data": user_data
            }
        }
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "data": "NotFound"
            }
        }

    return Response(response_data, status=status.HTTP_200_OK)


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
                "message":"NotFound",
                "data":[]
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def student_register(request):
    # uploaded_image = request.FILES.get('image')
    serializer = StudentSerializer(data=request.data)
    
    if serializer.is_valid():
        admission_number = request.data['admission_number']
        roll_number = request.data['roll_number']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        date_of_birth = request.data['date_of_birth']
        address = request.data['address']
        gender = request.data['gender']
        phone = request.data['phone']
        email = request.data['email']
        marital_status = request.data['marital_status']
        admission_year = request.data['admission_year']
        parent_name = request.data['parent_name']
        parent_phone_number = request.data['parent_phone_number']
        parent_email = request.data['parent_email']
        program_id = request.data['program_id']
        username = request.data['username']
        password = request.data['password']
        # image = request.data['image']
        
        if not Student.objects.filter(admission_number=admission_number).exists():
            if Programs.objects.filter(id=program_id).exists():
                program = Programs.objects.get(id=program_id)
                
                dob = datetime.strptime(date_of_birth, '%d-%m-%Y').strftime('%Y-%m-%d')
                student = Student.objects.create(
                    admission_number=admission_number,
                    roll_number=roll_number,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=dob,
                    address=address,
                    gender=gender,
                    phone=phone,
                    email=email,
                    marital_status=marital_status,
                    admission_year=admission_year,
                    parent_name=parent_name,
                    parent_phone_number=parent_phone_number,
                    parent_email=parent_email,
                    program=program,
                    username=username,
                    password=password,
                    # image=image    
                ) 
                no_of_semester=Programs.objects.get(id=program_id).number_of_semester
                for i in range(1,no_of_semester+1):
                    sem_starting='Semester '+str(i)
                    sem=Semesters.objects.get(semester=sem_starting)
                    program_sem=Program_Semester.objects.get(program_id=program_id,semester=sem)
                    Student_program_semester.objects.create(student=student,semester=program_sem,status="upcoming")                
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "message":"Registered SuccessFully"
                    }
                }
            else:
                response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":"Program not Exists"
                }
            }      
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":"This Admission number already Exists"
            }
        }
    else: 
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": "Registration failed.",
                "errors": serializer.errors
            }
        }       
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def students(request):
    ids_param = request.query_params.get("ids")
    
    if ids_param:
        ids_list = [int(id) for id in ids_param.strip("[]").split(",")]
        if Student.objects.filter(id__in=ids_list):
            
            
            students = Student.objects.filter(id__in=ids_list)
            serializer = StudentListSerializer(students, many=True)
            response_data = {
                "statusCode": 6000,
                "data": {
                    "title": "Success",
                    "data": serializer.data
                }
            }
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"student not found",
                "data":[]
            }
        }
    else:
        if Student.objects.all():
            students = Student.objects.all()  # Fetch all students if no ids parameter is provided
            serializer = StudentListSerializer(students, many=True)
            response_data = {
                "statusCode": 6000,
                "data": {
                    "title": "Success",
                    "data": serializer.data
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":"student not found",
                    "data":[]
                }
            }
    
    
    return Response(response_data, status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([AllowAny])
def student_details(request, pk):
    if Student.objects.filter(id=pk).exists():
        student = Student.objects.get(id=pk)
        serializer = StudentListSerializer(student, many=False)
        
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
                "message":"student not found",
                "data":[]
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

    
@api_view(["POST"])
@permission_classes([AllowAny])
def student_document_upload(request):
    serializer = StudentDocumentsSerializer(data=request.data)
    
    if serializer.is_valid():
        student_id = request.data['student']
        document_type = request.data['document_type']
        document_file = request.data['document_file']
        mark = request.data['mark']
        
        if Student.objects.filter(id=student_id).exists():
            student = Student.objects.get(id=student_id)
            StudentDocument.objects.create(
                student=student,
                document_type=document_type,
                document_file=document_file,
                mark=mark           
                )
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "message":"Uploaded SuccessFully"
                }
            }      
            
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"This student not Exists",
                "data":[]
            }
        }
    else: 
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": "Upload failed.",
                "errors": serializer.errors
            }
        }       
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(["GET"])
@permission_classes([AllowAny])
def student_documents(request):
    if StudentDocument.objects.all():
        documents = StudentDocument.objects.all()
        serializer = StudentDocumentsSerializer(documents, many=True)
        
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
                "message":"NotFound",
                "data":[]
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def student_document_details(request, pk):
    if StudentDocument.objects.filter(id=pk).exists():
        document = StudentDocument.objects.get(id=pk)
        serializer = StudentDocumentsSerializer(document, many=False)
        
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
                "message":"student not found",
                "data":[]
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def student_register_with_documents(request):
    # uploaded_image = request.FILES.get('image')
    serializer = StudentSerializer(data=request.data)
    
    if serializer.is_valid():
        admission_number = request.data['admission_number']
        roll_number = request.data['roll_number']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        date_of_birth = request.data['date_of_birth']
        address = request.data['address']
        gender = request.data['gender']
        phone = request.data['phone']
        email = request.data['email']
        marital_status = request.data['marital_status']
        admission_year = request.data['admission_year']
        parent_name = request.data['parent_name']
        parent_phone_number = request.data['parent_phone_number']
        parent_email = request.data['parent_email']
        program_id = request.data['program_id']
        username = request.data['username']
        password = request.data['password']
        # image = request.data['image'] //addd more fields 
        
        if not Student.objects.filter(admission_number=admission_number).exists():
            if Programs.objects.filter(id=program_id).exists():
                program = Programs.objects.get(id=program_id)
                
                dob = datetime.strptime(date_of_birth, '%d-%m-%Y').strftime('%Y-%m-%d')
                student = Student.objects.create(
                    admission_number=admission_number,
                    roll_number=roll_number,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=dob,
                    address=address,
                    gender=gender,
                    phone=phone,
                    email=email,
                    marital_status=marital_status,
                    admission_year=admission_year,
                    parent_name=parent_name,
                    parent_phone_number=parent_phone_number,
                    parent_email=parent_email,
                    program=program,
                    username=username,
                    password=password,
                    # image=image    
                ) 
                no_of_semester=Programs.objects.get(id=program_id).number_of_semester
                for i in range(1,no_of_semester+1):
                    sem_starting='Semester '+str(i)
                    sem=Semesters.objects.get(semester=sem_starting)
                    program_sem=Program_Semester.objects.get(program_id=program_id,semester=sem)
                    Student_program_semester.objects.create(student=student,semester=program_sem,status="upcoming")                
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "message":"Registered SuccessFully"
                    }
                }
            else:
                response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":"Program not Exists"
                }
            }      
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":"This Admission number already Exists"
            }
        }
    else: 
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Validation Error",
                "message": "Registration failed.",
                "errors": serializer.errors
            }
        }       
    return Response(response_data,status=status.HTTP_200_OK)