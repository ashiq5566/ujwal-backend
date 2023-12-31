
import requests
import json
from django.contrib.auth.models import Group
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from django.db.models import Max, F
from datetime import timedelta, datetime, timezone,date

from .serializers import *
from api.v1.accounts.functions import authenticate
from accounts.models import User
from main.models import *
from django.db.models import Subquery
from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from api.v1.main.decorators import group_required

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
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

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def edit_department(request, pk):
    """
    View function to get details of particular department.

    """ 
    if Departments.objects.filter(pk=pk).exists():
        department = Departments.objects.get(pk=pk)
        serializer = DepartmentPostSerializer(department, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
        
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "message":"Updated successfully",
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":serializer._errors
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"Department not found"
            }
        }
            
    
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def department_list(request):
    if Departments.objects.all():
        departments = Departments.objects.all().order_by('department_name')  
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get_department_instance(request,pk):
    if Departments.objects.filter(id=pk).exists():
        department = Departments.objects.filter(id=pk)
        serializer = DepartmentsGetSerializer(department, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def add_trainer(request):
    serializer = TrainerPostSerializer(data=request.data)
    
    if serializer.is_valid():
        
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Trainer created successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Trainer creation failed.",
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def edit_trainer(request, pk):
    """
    View function to get details of particular trainer.

    """ 
    if Trainers.objects.filter(pk=pk).exists():
        trainer = Trainers.objects.get(pk=pk)
        serializer = TrainerPostSerializer(trainer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
        
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "message":"Updated successfully",
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":serializer._errors
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"trainer not found"
            }
        }
            
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def trainers_list(request):
    if Trainers.objects.all():
        trainers = Trainers.objects.all().order_by('-id')  
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
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
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def edit_recruiter(request, pk):
    """
    View function to get details of particular recruiter.

    """ 
    if Recruiters.objects.filter(pk=pk).exists():
        recruiter = Recruiters.objects.get(pk=pk)
        serializer = RecruiterPostSerializer(recruiter, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
        
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "message":"Updated successfully",
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":serializer._errors
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"recruiter not found"
            }
        }
            
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def recruiters_list(request):
    if Recruiters.objects.filter().exists():
        recruiter = Recruiters.objects.all().order_by('-id')
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
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
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def edit_program(request, pk):
    """
    View function to get details of particular program.

    """ 
    if Programs.objects.filter(pk=pk).exists():
        program = Programs.objects.get(pk=pk)
        department_id = request.data.get('department')
        if Departments.objects.filter(id=department_id).exists():
            dep = Departments.objects.get(id=department_id)
        if(not dep.is_active):
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":"Cannot Proceed. Department is Inactive",
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = ProgramPostSerializer(program, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
        
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "message":"Updated successfully",
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":serializer._errors
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"program not found"
            }
        }
            
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def program_list(request):
    if Programs.objects.filter(is_active=True).exists():
        programs = Programs.objects.filter(is_active=True).order_by('program_name')
        serializer = ProgramsGetWithDepartmentSerializer(programs, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
def program_list_without_permission(request):
    if Programs.objects.filter(is_active=True).exists():
        programs = Programs.objects.filter(is_active=True).order_by('program_name')
        serializer = ProgramsGetWithDepartmentSerializer(programs, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def update_program(request, program_id):
    try:
        program_instance = Programs.objects.get(id=program_id)
    except Programs.DoesNotExist:
        response_data = {
            "statusCode": 6001,
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
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def focusing_areas(request):
    if FocusingArea.objects.all():
        focusingArea = FocusingArea.objects.all()  
        serializer = FocusinAreaGetSerializer(focusingArea, many=True)
        
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def programs_by_department(request, pk):
    if Departments.objects.filter(id=pk).exists():
        department = Departments.objects.get(id=pk)
        program=Programs.objects.filter(department=department)
        serializer = ProgramsGetSerializer(program, many=True)
        
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def semesters(request):
    if Semesters.objects.all():
        semesters = Semesters.objects.all()  
        serializer = SemestersGetSerializer(semesters, many=True)
        
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def program_semester_by_program(request, pk):
    if Programs.objects.filter(id=pk).exists():
        program = Programs.objects.get(id=pk)
        program_semester=Program_Semester.objects.filter(program=program)
        serializer = ProgramSemesterGetSerializer(program_semester, many=True)
        
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def program_semesters(request):
    if Program_Semester.objects.all():
        program_Semester = Program_Semester.objects.all()  
        serializer = ProgramSemesterGetSerializer(program_Semester, many=True)
        
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


@api_view(['POST'])
@permission_classes([AllowAny,])
def add_training_schedule(request):
    serializer = TrainingScheduleSerializer(data=request.data)
    if serializer.is_valid():
        trainer_id = request.data['trainer_id']
        start_date_str = request.data['start_date_str']
        created_date_str = request.data['created_date_str']
        end_date_str = request.data['end_date_str']
        venue = request.data['venue']
        foc_areas_ids = request.data['foc_areas_ids']
        participants_ids = request.data['participants_ids']
        
                
        if FocusingArea.objects.filter(id__in=foc_areas_ids).exists():
            foc_areas = FocusingArea.objects.filter(id__in=foc_areas_ids)
            if Trainers.objects.filter(id=trainer_id).exists():
                trainer = Trainers.objects.get(id=trainer_id)
                if Program_Semester.objects.filter(id__in=participants_ids).exists():
                    participants = Program_Semester.objects.filter(id__in=participants_ids)
                    
                    # Convert date string to the desired format
                    start_date = datetime.strptime(start_date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
                    end_date = datetime.strptime(end_date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
                    created_date = datetime.strptime(created_date_str, '%d-%m-%Y').strftime('%Y-%m-%d')

                    
                    allot_trainer=AllotTrainer(trainer=trainer,start_date=start_date,end_date=end_date,venue=venue,created_date=created_date)
                    allot_trainer.save()
                    allot_trainer.focusing_area.set(foc_areas) 

                    #Creating paricipence according to the traing allotment and store in TrainingParticipent model
                    for pgm_sem in participants:
                        participant = TrainingParticipant(
                            allot_trainer=allot_trainer,
                            program_semester=pgm_sem
                        )
                        participant.save()

                    response_data = {
                        'statusCode' : 6000,
                        'data' : {
                            'title': 'Success',
                            'message' : "Schedule Added SuccessFully"
                        }
                    }
                else:
                    response_data = {
                        'statusCode' : 6001,
                        'data' : {
                            'title': 'failed',
                            'message' : "Participants Not Found",
                            "data":[]
                        }
                    }
            else:
                response_data = {
                    'statusCode' : 6001,
                    'data' : {
                        'title': 'failed',
                        'message' : "Trainer Not Found",
                        "data":[]
                    }
                } 
        else:
            response_data = {
                'statusCode' : 6001,
                'data' : {
                    'title': 'failed',
                    'message' : "Focusing Area Not Found",
                    "data":[]
                }
            }
    else:
         response_data = {
            "statusCode": 6001,
            "title": "Validation Error",
            "message": serializer._errors,
            "data":[]
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def edit_training_schedule(request, pk):
    """
    View function to get details of particular schedule.

    """ 
    if AllotTrainer.objects.filter(pk=pk).exists():
        schedule = AllotTrainer.objects.get(pk=pk)
        serializer = EditTrainingScheduleSerializer(schedule, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(serializer.instance, serializer.validated_data)
        
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "message":"Updated successfully",
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":serializer._errors
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"Schedule not found"
            }
        }
            
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny,])
def training_schedule(request): 
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    department_id = request.GET.get('department_id')
    if start_date and end_date and department_id:
        if AllotTrainer.objects.filter(start_date__range=(start_date, end_date)).exists():
            schedule = AllotTrainer.objects.filter(start_date__range=(start_date, end_date)).order_by('-start_date')
            allot_trainers_with_participants = schedule.prefetch_related(
                'trainingparticipant_set__program_semester'
            )
            data=[]
            for allot_trainer in allot_trainers_with_participants:
                focusing_areas = [area.area_name for area in allot_trainer.focusing_area.all()]
                instance={
                    'id':allot_trainer.id,
                    "trainer_name":allot_trainer.trainer.trainer_name,
                    "focusing_area":focusing_areas,
                    "training_company":allot_trainer.trainer.training_company,
                    "training_company":allot_trainer.trainer.training_company,
                    "venue":allot_trainer.venue,
                    "start_date":allot_trainer.start_date.isoformat() if allot_trainer.start_date else None ,
                    "end_date":allot_trainer.end_date.isoformat() if allot_trainer.end_date else None,
                    "status":allot_trainer.status
                    }
                pgmSems=[]
                departmentCheck=False
                for training_participant in allot_trainer.trainingparticipant_set.all():
                    department_id = int(department_id)
                    if training_participant.program_semester.program.department.id == department_id:
                        departmentCheck=True
                    pgmSem={
                        "id":training_participant.id,
                        "program_semester":training_participant.program_semester.id,
                        "department":training_participant.program_semester.program.department.id,
                        "department_name":training_participant.program_semester.program.department.department_name,
                        "program":training_participant.program_semester.program.id,
                        "program_name":training_participant.program_semester.program.program_name,
                        "semester":training_participant.program_semester.semester.id,
                        "semester_name":training_participant.program_semester.semester.semester
                    }
                    if training_participant.program_semester.program.department.id==department_id:
                        pgmSems.append(pgmSem)
                        print(training_participant.program_semester.program.department.id,department_id,"department_iddepartment_iddepartment_id")

                instance["program_semesters"]=pgmSems
                if departmentCheck:
                    data.append(instance)

            json_data = json.dumps(data, indent=4)
            
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":json_data
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":"Schedule Not Found",
                    "data":[]
                }
            }
    elif start_date and end_date:
        if AllotTrainer.objects.filter(start_date__range=(start_date, end_date)).exists():
            schedule = AllotTrainer.objects.filter(start_date__range=(start_date, end_date)).order_by('-start_date')
            allot_trainers_with_participants = schedule.prefetch_related(
                'trainingparticipant_set__program_semester'
            )
            data=[]
            for allot_trainer in allot_trainers_with_participants:
                focusing_areas = [area.area_name for area in allot_trainer.focusing_area.all()]
                instance={
                    'id':allot_trainer.id,
                    "trainer_name":allot_trainer.trainer.trainer_name,
                    "focusing_area":focusing_areas,
                    "training_company":allot_trainer.trainer.training_company,
                    "training_company":allot_trainer.trainer.training_company,
                    "venue":allot_trainer.venue,
                    "start_date":allot_trainer.start_date.isoformat() if allot_trainer.start_date else None,
                    "end_date":allot_trainer.end_date.isoformat() if allot_trainer.end_date else None,
                    "status":allot_trainer.status
                    }
                pgmSems=[]
                for training_participant in allot_trainer.trainingparticipant_set.all():
                    pgmSem={
                        "id":training_participant.id,
                        "program_semester":training_participant.program_semester.id,
                        "department":training_participant.program_semester.program.department.id,
                        "department_name":training_participant.program_semester.program.department.department_name,
                        "program":training_participant.program_semester.program.id,
                        "program_name":training_participant.program_semester.program.program_name,
                        "semester":training_participant.program_semester.semester.id,
                        "semester_name":training_participant.program_semester.semester.semester
                    }
                    pgmSems.append(pgmSem)
                instance["program_semesters"]=pgmSems
                data.append(instance)

            json_data = json.dumps(data, indent=4)
            
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":json_data
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":"Schedule Not Found",
                    "data":[]
                }
            }
    else:
        response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Invalied batch"
                }
            }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny,])
def training_schedule_detail(request, pk):
    if AllotTrainer.objects.filter(id=pk).exists():
        schedule = AllotTrainer.objects.get(id=pk)   
        serializer = TrainingSchedulesSerializer(schedule, many=False)
        
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
                "message":"Schedule Not Found",
                "data":[]
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny,])
def add_recruitment_schedule(request):
    serializer = RecruitmentScheduleSerializer(data=request.data)
    
    if serializer.is_valid():
        recruiter_id = request.data['recruiter_id']
        date_str = request.data['date']  
        venue = request.data['venue']
        designation = request.data['designation']
        participants_ids = request.data['participants_ids']
        apply_link = request.data['apply_link']
        number_of_hirings = request.data['number_of_hirings']
        apply_last_date_str = request.data['apply_last_date']
        description = request.data['description']


        
        if Recruiters.objects.filter(id=recruiter_id).exists():
            recruiter = Recruiters.objects.get(id=recruiter_id)
            if Program_Semester.objects.filter(id__in=participants_ids).exists():
                participants = Program_Semester.objects.filter(id__in=participants_ids)
                date = datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
                apply_last_date = datetime.strptime(apply_last_date_str, '%d-%m-%Y').strftime('%Y-%m-%d')

                
                allot_recruiter = Schedule_Recruitment(recruiter=recruiter,
                    date=date,
                    venue=venue,
                    designation=designation,
                    apply_link=apply_link,
                    number_of_hirings=number_of_hirings,
                    apply_last_date=apply_last_date,
                    description=description
                )
                allot_recruiter.save()
                
                recruitment_branch = Recruitment_Participating_Branches(scheduled_recruitment=allot_recruiter)
                recruitment_branch.save()
                recruitment_branch.program_semester.set(participants)
                response_data = {
                    'statusCode' : 6000,
                    'data' : {
                        'title': 'Success',
                        'message' : "Schedule Added SuccessFully"
                    }
                }
            else:
                response_data = {
                'statusCode' : 6001,
                'data' : {
                    'title': 'failed',
                    'message' : "Participants Not Found",
                    "data":[]
                }
            }
        else:
            response_data = {
                'statusCode' : 6001,
                'data' : {
                    'title': 'failed',
                    'message' : "Recruiter Not Found",
                    "data":[]
                }
            }
    else:
         response_data = {
            "statusCode": 6001,
            "title": "Validation Error",
            "message": serializer._errors,
            "data":[]
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_schedule(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    department_id = request.GET.get('department_id')
    if start_date and end_date and department_id:
        recruitment_branches = Recruitment_Participating_Branches.objects.filter(
                                    scheduled_recruitment__date__range=(start_date, end_date),program_semester__program__department__id=department_id
                                )
        scheduled_recruitment_ids = recruitment_branches.values_list('scheduled_recruitment__id', flat=True)
        if Schedule_Recruitment.objects.filter(date__range=(start_date, end_date)).exists():
            schedule =  Schedule_Recruitment.objects.filter(id__in=scheduled_recruitment_ids).order_by('-date')
            serializer = RecruitmentSchedulesSerializer(schedule, many=True)
            
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
                    "message":"Schedule Not Found",
                    "data":[]
                }
            }
    elif start_date and end_date:
        if Schedule_Recruitment.objects.filter(date__range=(start_date, end_date)).exists():
            schedule =  Schedule_Recruitment.objects.filter(date__range=(start_date, end_date)).order_by('-date')
            serializer = RecruitmentSchedulesSerializer(schedule, many=True)
            
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
                    "message":"Schedule Not Found",
                    "data":[]
                }
            }
    else:
        response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Invalied batch"
                }
            }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_schedule_detail(request, pk):
    if Schedule_Recruitment.objects.filter(id=pk).exists():
        schedule = Schedule_Recruitment.objects.get(id=pk)   
        serializer = RecruitmentSchedulesSerializer(schedule, many=False)
        
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
                "message":"Schedule Not Found",
                "data":[]
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def training_participents_details(request):
    department_id = request.GET.get('department_id')
    allot_tariner_id = request.GET.get('allot_tariner_id')
    if allot_tariner_id:
        allot_tariner_id = int(allot_tariner_id)
        if department_id:
            department_id = int(department_id)
            training_participant = TrainingParticipant.objects.filter(allot_trainer__id=allot_tariner_id,program_semester__program__department__id=department_id) 
        else:
            training_participant = TrainingParticipant.objects.filter(allot_trainer__id=allot_tariner_id) 
        serializer = TrainingParticipentsSerializer(training_participant, many=True)
        
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":serializer.data
            }
        }
    elif TrainingParticipant.objects.all():
        training_participant = TrainingParticipant.objects.all()  
        serializer = TrainingParticipentsSerializer(training_participant, many=True)
        
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def recruitment_participents_details(request):
    if Recruitment_Participating_Branches.objects.all():
        recruitment_participant = Recruitment_Participating_Branches.objects.all()  
        serializer = RecruitmentParticipentsSerializer(recruitment_participant, many=True)
        
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


@api_view(['POST'])
@permission_classes([AllowAny,])
def attendance(request, pk):
    serializer = AttendancePostSerializer(data=request.data)
    
    if serializer.is_valid():
        if TrainingParticipant.objects.filter(id=pk).exists():
            training_participant=TrainingParticipant.objects.get(id=pk)
            present_student_ids = request.data['present_student']
            absent_student_ids = request.data['absent_student']
            present_students = Student.objects.filter(id__in=present_student_ids)
            absent_students = Student.objects.filter(id__in=absent_student_ids)
            responce_date = request.data['date']
            attendance_instance = Attendence.objects.create(
                training_participant=training_participant,
                date=responce_date
                )
            attendance_instance.present_students.set(present_students)
            attendance_instance.absent_student.set(absent_students)
            response_data = {
                    "statusCode": 6000,
                    "data":{
                        "title": "Success",
                        "message": "Attendence Added SuccessFully"
                    }
                }
        else:
            response_data = {
                            "statusCode": 6001,
                            "data":{
                                "title": "Failed",
                                "message": "Attendence marking failed",
                                "data":[]
                            }
                        }
    else:
        response_data = {
        "statusCode": 6001,
        "data":{
            "title": "Validation Error",
            "message": serializer._errors,
            "data":[]
        }
    }  
    return Response(response_data,status=status.HTTP_200_OK) 


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def student_program_semester_details(request):
    
    date = request.GET.get('date')
    program_semester_id = request.GET.get('program_semester_id')

    if date and program_semester_id:
        results = Student_program_semester.objects.filter(
        Q(semester_id=program_semester_id) & (
            Q(start_date__isnull=False, end_date__isnull=True) |
            Q(start_date__isnull=False, end_date__isnull=False, start_date__lte=date, end_date__gte=date)
        )
        )
        serializer = StudentProgramSemesterSerializer(results, many=True)
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":serializer.data
            }
        }
    else:
        if Student_program_semester.objects.all():
            student_program_semester = Student_program_semester.objects.all()  
            serializer = StudentProgramSemesterSerializer(student_program_semester, many=True)
            
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


@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_applied_students_by_recruitment_schedule(request, pk):
    department_id = request.GET.get('department_id')
    if department_id:
        if Recruitment_Participated_Students.objects.filter(scheduled_recruitment_id=pk,student__program__department__id=department_id).exists():
            students =Recruitment_Participated_Students.objects.filter(scheduled_recruitment_id=pk,student__program__department__id=department_id)
            serializer = RecruitmentParticipatedStudentsSchedulesSerializer(students, many=True)

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
                "message":"Participated student list Not Found",
                "data":[]
                }
            }

    elif Recruitment_Participated_Students.objects.filter(scheduled_recruitment_id=pk).exists():
        students =Recruitment_Participated_Students.objects.filter(scheduled_recruitment_id=pk)
        serializer = RecruitmentParticipatedStudentsSchedulesSerializer(students, many=True)

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
                "message":"Participated student list Not Found",
                "data":[]
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny,])
def student_program_semester_by_program_semester(request, pk):
    if Program_Semester.objects.filter(id=pk).exists():
        students_program_semester =Student_program_semester.objects.filter(semester_id=pk)
        serializer = StudentProgramSemesterSerializer(students_program_semester, many=True)
        
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
                "message":"Program semester Not Found",
                "data":[]
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def add_recruitment_Participated_Students(request):
    serializer = PostRecruitmentParticipatedStudentsSchedulesSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Recruitment participating student added successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Recruitment participatindg student adding failed.",
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def attendenceMarkedOrNot(request):
    
    date = request.GET.get('date')
    training_Participent = request.GET.get('trainingParticipent_id')

    if date and training_Participent:
        result=Attendence.objects.filter(training_participant=training_Participent,date=date).exists()
        if(result):
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":{
                        "attendenceMarked":True
                    }
                }
            }
        else:
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":{
                        "attendenceMarked":False
                    }
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Error",
                "message": "Date and trainer id not found",
                "data": []
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def ongoing_program_semester_promote_details(request):
    department_id = request.GET.get('department_id')
    if department_id:
        ongoing_semester_ids = list(set([i.semester.id for i in Student_program_semester.objects.filter(status='ongoing')]))
        
        upcoming_new_sem_ids=[]
        for i in Student_program_semester.objects.filter(status='upcoming'):
            for j in Program_Semester.objects.filter(id=i.semester.id):
                sem_1=Semesters.objects.get(semester="Semester 1")
                if j.semester.id==sem_1.id:
                    upcoming_new_sem_ids += [i.semester.id]
        upcoming_new_sem_ids=list(set(upcoming_new_sem_ids))
        upcoming_details=[]
        department_id = int(department_id)
        for unpsId in upcoming_new_sem_ids:
            instance_upcoming = Program_Semester.objects.get(id=unpsId)
            if instance_upcoming.program.department.id==department_id:
                instance_upcoming_data={
                    "id":unpsId,
                    "program":instance_upcoming.program.id,
                    "program_name":instance_upcoming.program.program_name,
                    "semester":instance_upcoming.semester.id,
                    "semester_name":instance_upcoming.semester.semester
                }
                upcoming_details.append(instance_upcoming_data)
        json_upcoming_data=json.dumps(upcoming_details, indent=4)

        ongoing_details=[]
        for ogpsId in ongoing_semester_ids:
            instance_ongoing = Program_Semester.objects.get(id=ogpsId)
            if instance_ongoing.program.department.id==department_id:
                instance_ongoing_data={
                    "id":ogpsId,
                    "program":instance_ongoing.program.id,
                    "program_name":instance_ongoing.program.program_name,
                    "semester":instance_ongoing.semester.id,
                    "semester_name":instance_ongoing.semester.semester
                }
                ongoing_details.append(instance_ongoing_data)
        json_ongoing_data=json.dumps(ongoing_details, indent=4)

        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":{
                    "onGoingProgramSemesters": json_ongoing_data,
                    "upcomingBatchFirstProgramSemesters":json_upcoming_data
                }
            }
        }
    elif Student_program_semester.objects.filter().exists():
        ongoing_semester_ids = list(set([i.semester.id for i in Student_program_semester.objects.filter(status='ongoing')]))
        
        upcoming_new_sem_ids=[]
        for i in Student_program_semester.objects.filter(status='upcoming'):
            for j in Program_Semester.objects.filter(id=i.semester.id):
                sem_1=Semesters.objects.get(semester="Semester 1")
                if j.semester.id==sem_1.id:
                    upcoming_new_sem_ids += [i.semester.id]
        upcoming_new_sem_ids=list(set(upcoming_new_sem_ids))
        upcoming_details=[]
        for unpsId in upcoming_new_sem_ids:
            instance_ongoing = Program_Semester.objects.get(id=unpsId)
            instance_ongoing_data={
                "id":unpsId,
                "program":instance_ongoing.program.id,
                "program_name":instance_ongoing.program.program_name,
                "semester":instance_ongoing.semester.id,
                "semester_name":instance_ongoing.semester.semester
            }
            upcoming_details.append(instance_ongoing_data)
        json_upcoming_data=json.dumps(upcoming_details, indent=4)

        ongoing_details=[]
        for ogpsId in ongoing_semester_ids:
            instance_ongoing = Program_Semester.objects.get(id=ogpsId)
            instance_ongoing_data={
                "id":ogpsId,
                "program":instance_ongoing.program.id,
                "program_name":instance_ongoing.program.program_name,
                "semester":instance_ongoing.semester.id,
                "semester_name":instance_ongoing.semester.semester
            }
            ongoing_details.append(instance_ongoing_data)
        json_ongoing_data=json.dumps(ongoing_details, indent=4)

        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":{
                    "onGoingProgramSemesters": json_ongoing_data,
                    "upcomingBatchFirstProgramSemesters":json_upcoming_data
                }
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Error",
                "message": "No Program semester Exists",
                "data": []
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_Student_UpdationDetails_by_Participated_Student(request, pk):
    if Recruitment_Participated_Students.objects.filter(id=pk).exists():
        participatedStudent = Recruitment_Participated_Students.objects.get(id=pk) 
        selections=Recruitment_Student_Updations.objects.filter(recruitment_participated_student=participatedStudent)  
        serializer = RecruitmentSelectionUpdatesSchedulesSerializer(selections, many=True)
        
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
                "message":"Student Not Found",
                "data":[]
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_Student_UpdationDetails_by_List_of_Student(request):
    # Get the list of IDs from the query parameter, e.g., /your-endpoint/?ids=6,7,8,9
    ids_list = request.GET.get('ids')
    ids_list = [int(id) for id in ids_list.strip('[]').split(',') if id]
    
    if not ids_list:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "No student IDs provided",
                "data":[]
            }
        }
    else:   
        selections =  Recruitment_Student_Updations.objects.filter(recruitment_participated_student__id__in=ids_list)
        if selections.exists():
            serializer = RecruitmentSelectionUpdatesSchedulesSerializer(selections, many=True)

            response_data = {
                "statusCode": 6000,
                "data": {
                    "title": "Success",
                    "data": serializer.data
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "statusCode": 6001,
                "data": {
                    "title": "Failed",
                    "message": "Students Not Found",
                    "data":[]
                }
            }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def add_selection_update_for_student(request):
    serializer = RecruitmentSelectionUpdatesSchedulesSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Selection update added successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Selection update adding failed.",
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny,])
def get_participatedStudents_for_placement_by_schedule(request,pk):
    if Schedule_Recruitment.objects.filter(id=pk).exists():
        schedule=Schedule_Recruitment.objects.get(id=pk)
        if(Recruitment_Participated_Students.objects.filter(scheduled_recruitment=schedule).exists()):
            students = Recruitment_Participated_Students.objects.filter(scheduled_recruitment=schedule) \
                    .exclude(id__in=Subquery(Placed_students.objects.values('recruitment_participated_student_id')))
            serializer = ParticipatedStudentsByRecruitmentSchedulesSerializer(students,many=True)
            response_data = {
                    "statusCode": 6000,
                    "data": {
                        "title": "Success",
                        "data": serializer.data
                    }
                }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                    "statusCode": 6000,
                    "data": {
                        "title": "Success",
                        "data": []
                    }
                }
            return Response(response_data, status=status.HTTP_200_OK)
        
    response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Recruitment Schedule not found",
                "data":[]
            }
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def add_a_placement(request):
    serializer = PlacedPOSTStudentsSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Placement added successfully."
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
        "statusCode": 6001,
        "data": {
            "title": "Validation Error",
            "message": "Selection update adding failed.",
            "errors": serializer.errors,
            "data":[]
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny,])
def promote_current_batch(request, pk):
    program =Program_Semester.objects.get(id=pk).program
    semester = Program_Semester.objects.get(id=pk).semester
    semNumber=Semesters.objects.get(id=semester.id).semester
    if Semesters.objects.filter(semester='Semester '+str(int(semNumber[9:])+1)).exists():
        nextSem=Semesters.objects.get(semester='Semester '+str(int(semNumber[9:])+1))
        if Program_Semester.objects.filter(program_id=program.id,semester_id=nextSem.id).exists():
            nextSem_id=Program_Semester.objects.get(program_id=program.id,semester_id=nextSem.id)
            ongoing_students = Student_program_semester.objects.filter(semester=pk, status="ongoing")
            if  Student_program_semester.objects.filter(semester=nextSem_id.id,status="ongoing").count()>0:
                response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "message":"Already there exists a Program semester",
                    "data":[]
                    }
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            Student_program_semester.objects.filter(
                                semester=nextSem_id.id,
                                status="upcoming",
                                student__in=ongoing_students.values_list('student', flat=True)
                                ).update(status="ongoing", start_date=datetime.now().date() + timedelta(days=1))
            Student_program_semester.objects.filter(semester=pk, status="ongoing").update(status="completed",end_date=datetime.now())
            # Student_program_semester.objects.filter(semester=nextSem_id,status="upcoming",student__in=Subquery(ongoing_students)).update(status="ongoing", start_date=datetime.now().date() + timedelta(days=1))
        else:
            Student_program_semester.objects.filter(semester=pk,status="ongoing").update(status="completed",end_date=datetime.now())
    else:
        Student_program_semester.objects.filter(semester=pk,status="ongoing").update(status="completed",end_date=datetime.now())

    response_data = {
        "statusCode":6000,
        "data":{
            "title":"Success",
            "message":"Program semester promoted succesfully"
        }
    }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([AllowAny,])
def promote_new_batch(request, pk):
    program =Program_Semester.objects.get(id=pk).program
    semester = Program_Semester.objects.get(id=pk).semester
    if(Student_program_semester.objects.filter(semester=pk, status="upcoming").exists()):
        if Student_program_semester.objects.filter(semester=pk, status="ongoing").count()>0:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"Already there exists a Program semester",
                "data":[]
                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            students = Student_program_semester.objects.filter(semester=pk, status="upcoming")
            for student in students:
                student_username=Student.objects.get(id=student.student.id).username
                User.objects.filter(username=student_username).update(is_active=True)
            Student_program_semester.objects.filter(semester=pk, status="upcoming").update(status="ongoing",start_date=datetime.now())


    response_data = {
        "statusCode":6000,
        "data":{
            "title":"Success",
            "message":"Program semester promoted succesfully"
        }
    }
    return Response(response_data,status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([AllowAny,])
# def get_placedStudents_by_year(request):
#     today = date.today()
#     if today.month < 6:  # If current month is before June, the academic year starts from the previous year
#         academic_year_start = date(today.year - 1, 6, 1)
#         academic_year_end = date(today.year, 5, 31)
#     else:  # Otherwise, it starts from the current year
#         academic_year_start = date(today.year, 6, 1)
#         academic_year_end = date(today.year + 1, 5, 31)

#     # Query to get the latest academic year's recruitment_participated_student details
#     latest_academic_year_details = Placed_students.objects.filter(
#         placed_date__gte=academic_year_start,
#         placed_date__lte=academic_year_end
#     ).annotate(
#         max_placed_date=Max('recruitment_participated_student__placed_students__placed_date')
#     ).filter(
#         placed_date=F('max_placed_date')
#     ).select_related('recruitment_participated_student')
        
#     response_data = {
#             "statusCode": 6001,
#             "data": {
#                 "title": "Failed",
#                 "message": "Recruitment Schedule not found",
#                 "data":[]
#             }
#         }
#     return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def getAttendence(request):
    
    date = request.GET.get('date')
    training_Participent = request.GET.get('trainingParticipent_id')

    if date and training_Participent:
        if(Attendence.objects.filter(training_participant=training_Participent,date=date).exists()):
            attendence =Attendence.objects.filter(training_participant=training_Participent,date=date)
            serializer = AttendanceSerializer(attendence, many=True)

            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":serializer.data
                }
            }
        else:
            response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Attendence Not available",
                "data":[]
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Error",
                "message": "Date and trainer id not found",
                "data":[]
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get_academic_years(request):
    current_date = date.today()
    academic_year_exists = Academic_year.objects.filter(start_date__lte=current_date, end_date__gte=current_date).exists()
    if not academic_year_exists:

        january_1st = date(date.today().year, 1, 1)
        may_31st = date(date.today().year, 5, 31)

        if january_1st <= current_date <= may_31st:
            # start_date = date(current_date.year - 1, 6, 1)
            # end_date = date(current_date.year, 5, 31)
            Academic_year.objects.create(start_date=date(current_date.year - 1, 6, 1), end_date=date(current_date.year, 5, 31))

        else:
            Academic_year.objects.create(start_date=date(current_date.year , 6, 1), end_date=date(current_date.year+1, 5, 31))
            # start_date = date(current_date.year , 6, 1)
            # end_date = date(current_date.year+1, 5, 31)

    if Academic_year.objects.all():
        academic_years = Academic_year.objects.all().order_by('-start_date')
        serializer = AcademicYearSerializer(academic_years, many=True)
        
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

@api_view(['GET'])
@permission_classes([AllowAny,])
def get_placedStudents_by_batch(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    department_id = request.GET.get('department_id')
    program_id = request.GET.get('program_id')
    if start_date and end_date and department_id:
        if Departments.objects.filter(id=department_id).exists():
            department = Departments.objects.get(id=department_id)
            placed_students = Placed_students.objects.filter(placed_date__range=(start_date, end_date),recruitment_participated_student__student__program__department=department).order_by('-placed_date')
            serializer = PlacedStudentsSerializer(placed_students, many=True)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":serializer.data
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"failed",
                    "data":[],
                    "message":"department not found",

                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    if start_date and end_date and program_id:
        if Programs.objects.filter(id=program_id).exists():
            program = Programs.objects.get(id=program_id)
            placed_students = Placed_students.objects.filter(placed_date__range=(start_date, end_date),recruitment_participated_student__student__program=program).order_by('-placed_date')
            serializer = PlacedStudentsSerializer(placed_students, many=True)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":serializer.data
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"failed",
                    "data":[],
                    "message":"program not found",

                }
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    if start_date and end_date:
        placed_students = Placed_students.objects.filter(placed_date__range=(start_date, end_date)).order_by('-placed_date')
        serializer = PlacedStudentsSerializer(placed_students, many=True)
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":serializer.data
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Not found",
                "data":[]
            }
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny,])
def complete_recruitment_schedule_status(request,pk):
    if Schedule_Recruitment.objects.filter(id=pk).exists():
        schedule=Schedule_Recruitment.objects.get(id=pk)
        schedule.status="completed"
        schedule.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Schedule updated Succesfully",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Schedule not exists",
                "data":[]
            }
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny,])
def cancel_recruitment_schedule_status(request,pk):
    if Schedule_Recruitment.objects.filter(id=pk).exists():
        schedule=Schedule_Recruitment.objects.get(id=pk)
        schedule.status="cancelled"
        schedule.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Schedule updated Succesfully",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Schedule not exists",
                "data":[]
            }
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([AllowAny,])
def complete_training_schedule_status(request,pk):
    if AllotTrainer.objects.filter(id=pk).exists():
        schedule=AllotTrainer.objects.get(id=pk)
        schedule.status="completed"
        schedule.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Schedule updated Succesfully",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Schedule not exists",
                "data":[]
            }
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([AllowAny,])
def cancel_training_schedule_status(request,pk):
    if AllotTrainer.objects.filter(id=pk).exists():
        schedule=AllotTrainer.objects.get(id=pk)
        schedule.status="cancelled"
        schedule.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Schedule updated Succesfully",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Schedule not exists",
                "data":[]
            }
        }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def getSkillSetByStudent(request,pk):
    if Student_skills.objects.filter(student__id=pk).exists():
        skill = Student_skills.objects.filter(student__id=pk)
        data = []  
        for i in skill:
            data.append(i.skill.skill_name)
        
        data=json.dumps(data, indent=4)

        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":data
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def add_skillset(request):
    # Get the skill and student IDs from the request data
    skill_id = request.data.get('skill')
    student_id = request.data.get('student')

    # Get the skill instance or create it if not found
    skill, created = Skills.objects.get_or_create(skill_name=skill_id)

    if not created:
        skill.save()

    # Get the student instance or return a 404 if not found
    student = get_object_or_404(Student, id=student_id)

    # Check if the skillset already exists for this student
    if Student_skills.objects.filter(student=student, skill=skill).exists():
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "failed",
                "message": "Skillset already exists",
                "data": []
            }
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # Create a new Student_skills instance
    student_skill = Student_skills.objects.create(student=student, skill=skill).save()

    response_data = {
        "statusCode": 6000,
        "data": {
            "title": "Success",
            "message": "Skillset added successfully.",
            "data": []
        }
    }
    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def get_placement_details_by_student(request,pk):
    student_id = int(pk)
    if Student_program_semester.objects.filter(student__id=student_id).exists():
        student_data=Student_program_semester.objects.filter(student__id=student_id)
        program_sems = []
        responce_date=[]
        for data in student_data:
            ps_instance ={
                "program_semester": data.semester,
                "start_date" : data.start_date,
                "end_date" : data.end_date,
                "status" : data.status,
            }
            program_sems.append(ps_instance)
        for program_sem in program_sems:
            if Recruitment_Participating_Branches.objects.filter(program_semester=program_sem['program_semester']).exists():
                part_batchs=(Recruitment_Participating_Branches.objects.filter(program_semester=program_sem['program_semester']))
                for part_batch in part_batchs:
                    
                    if program_sem['start_date'] and (program_sem['status']=='ongoing' or program_sem['status']=='completed' ) :
                        if program_sem['end_date']:
                            if program_sem['start_date'] <= part_batch.scheduled_recruitment.date <= program_sem['end_date']:
                                inst_res_data={
                                    "scheduled_recruitment":part_batch.scheduled_recruitment.id,
                                    "recruiter":part_batch.scheduled_recruitment.recruiter.id,
                                    "recruiter_name":part_batch.scheduled_recruitment.recruiter.company_name,
                                    "designation":part_batch.scheduled_recruitment.designation,
                                    "apply_link":part_batch.scheduled_recruitment.apply_link,
                                    "apply_last_date":part_batch.scheduled_recruitment.apply_last_date.isoformat() if part_batch.scheduled_recruitment.apply_last_date else None,
                                    "description":part_batch.scheduled_recruitment.description,
                                    "venue":part_batch.scheduled_recruitment.venue,
                                }
                                responce_date.append(inst_res_data)
                        elif program_sem['start_date'] <= part_batch.scheduled_recruitment.date:
                            inst_res_data={
                                "scheduled_recruitment":part_batch.scheduled_recruitment.id,
                                "recruiter":part_batch.scheduled_recruitment.recruiter.id,
                                "recruiter_name":part_batch.scheduled_recruitment.recruiter.company_name,
                                "designation":part_batch.scheduled_recruitment.designation,
                                "apply_link":part_batch.scheduled_recruitment.apply_link,
                                "apply_last_date":part_batch.scheduled_recruitment.apply_last_date.isoformat() if part_batch.scheduled_recruitment.apply_last_date else None,
                                "description":part_batch.scheduled_recruitment.description,
                                "venue":part_batch.scheduled_recruitment.venue,
                            }
                            responce_date.append(inst_res_data)
            responce_date_sent=json.dumps(sorted(responce_date, key=lambda x: x['apply_last_date'], reverse=True), indent=4)  

            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":responce_date_sent,
                }
            }             
                                
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def get_applied_placements_by_student(request,pk):
    student_id = int(pk)
    statusOfStudent = request.GET.get('status')
    if Recruitment_Participated_Students.objects.filter(student__id=student_id).exists():
        if statusOfStudent:
            appliedPlacements=Recruitment_Participated_Students.objects.filter(student__id=student_id,status=statusOfStudent)
        else:
            appliedPlacements=Recruitment_Participated_Students.objects.filter(student__id=student_id)

        data=[]
        for appliedPlacement in appliedPlacements:
            studentUpdationItems= Recruitment_Student_Updations.objects.filter(recruitment_participated_student=appliedPlacement)
            updationAll=[]
            for studentUpdationItem in studentUpdationItems:
                updationInstance={
                    "updation_date":studentUpdationItem.date.isoformat()  if studentUpdationItem.date else None,
                    "type_of_selection":studentUpdationItem.type_of_selection,
                    "selected_status":studentUpdationItem.is_selected,
                    "completed_status" :studentUpdationItem.status,
                    "others" :studentUpdationItem.others,
                    
                }
                updationAll.append(updationInstance)
            sorted_updationAll = sorted(updationAll, key=lambda x: x["updation_date"])
            instance = {
                "id" : appliedPlacement.id,
                "applied_date" :  appliedPlacement.applied_date.isoformat() if appliedPlacement.applied_date else None,
                "scheduled_recruitment_id" : appliedPlacement.scheduled_recruitment.id,
                "scheduled_recruitment_name" : appliedPlacement.scheduled_recruitment.recruiter.company_name,
                "designation" : appliedPlacement.scheduled_recruitment.designation,
                "status" : appliedPlacement.scheduled_recruitment.status,
                "student_process_details":sorted_updationAll,
                "placed_status" : Placed_students.objects.filter(recruitment_participated_student_id=appliedPlacement.id).exists(),
                "applied_status" : appliedPlacement.status
            }
            data.append(instance)
        responce_date_sent=json.dumps(data,indent=4)
        response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":responce_date_sent,
                }
            }   
        return Response(response_data,status=status.HTTP_200_OK)   

    response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def get_placed_result_by_student(request,pk):
    student_id = int(pk)
    if Placed_students.objects.filter(recruitment_participated_student__student__id=student_id).exists():
        student_placements= Placed_students.objects.filter(recruitment_participated_student__student__id=student_id)
        data=[]
        for student_placement in student_placements:
            instance={
                "id":student_placement.id,
                "student":student_placement.recruitment_participated_student.student.id,
                "recruiter":student_placement.recruitment_participated_student.scheduled_recruitment.recruiter.company_name,
                "designation":student_placement.recruitment_participated_student.scheduled_recruitment.designation,
                "placed_date":student_placement.placed_date.isoformat() if student_placement.placed_date else None,
                "offer_latter":student_placement.offer_latter.url if student_placement.offer_latter else None
            }
            data.append(instance)
        responce_date_sent=json.dumps(data,indent=4)
        response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":responce_date_sent,
                }
            }   
        return Response(response_data,status=status.HTTP_200_OK)  
    response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)
    
@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def upload_additional_document(request):
    if request.method == 'POST' and request.FILES.get('document'):
        student_id = request.data.get('student_id')
        student = Student.objects.get(pk=student_id)
        
        document = Student_Additional_Documents(
            student=student,
            document=request.FILES['document'],
            document_name=request.data.get('document_name')
        )
        document.save()
        
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Document added successfully.",
                "data": []
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def students_additional_documents(request,student_id):
    if Student_Additional_Documents.objects.filter(student_id=student_id).exists():
        docs = Student_Additional_Documents.objects.filter(student_id=student_id)
        serializer = StudentAdditionalDocumentsSerializer(docs, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def upload_resume(request):
    student_id = request.data.get('student_id')
    if request.method == 'POST' and request.FILES.get('resume') and Student.objects.filter(pk=student_id).exists():
        student = Student.objects.get(pk=student_id)
        existing_record, created = Student_Resume.objects.update_or_create(
            student=student,
            defaults={
                'resume': request.FILES['resume'],
            }
        )
        
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Resume updated successfully.",
                "data": []
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def student_resume(request,student_id):
    if Student_Resume.objects.filter(student_id=student_id).exists():
        docs = Student_Resume.objects.filter(student_id=student_id)
        serializer = StudentResumeSerializer(docs, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["PUT"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def update_offer_latter(request):
    placed_student_id = request.data.get('placed_student_id')
    salary_package= request.data.get('salary_package')
    new_offer_latter = request.FILES.get('offer_latter')
    if Placed_students.objects.filter(pk=placed_student_id).exists() and request.FILES.get('offer_latter'):
        placed_student = Placed_students.objects.get(pk=placed_student_id)
        placed_student.offer_latter = new_offer_latter
        placed_student.salary_package = salary_package
        placed_student.save()
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":[],
                "message":"Offer latter updated succesfully."
            }
        }
        
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"No student found."
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def dashboard_reports(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    placedStudents =[]
    placedInPrograms = []
    fiveYearReports = []
    
    if Placed_students.objects.filter().exists():
        placedStudents=Placed_students.objects.filter(recruitment_participated_student__applied_date__range=(start_date, end_date))
        programs=Programs.objects.filter(is_active=True)
        pgmPlcedList={}
        for pgm in programs:
            pgmPlcedList[pgm.program_name]=0
        for pgm in programs:
            for placStud in placedStudents:
                if(placStud.recruitment_participated_student.student.program.id==pgm.id):
                    pgmPlcedList[pgm.program_name]=pgmPlcedList[pgm.program_name]+1
        placedInPrograms=json.dumps(pgmPlcedList,indent=4)

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Initialize a dictionary to store the results
    fiveYearReport = {}

    # Iterate over the previous five years
    for i in range(5):
        academic_year = start_date.year+1
        previous_academic_year = academic_year-1 
        year_range = f"{academic_year}-{previous_academic_year}"
        
        # Count placed students within the academic year range
        placed_count = (
            Placed_students.objects
            .filter(placed_date__gte=start_date, placed_date__lt=end_date)
            .aggregate(count=Count('id'))
        )['count'] or 0

        fiveYearReport[year_range] = placed_count

        # Update start_date and end_date for the next iteration
        start_date -= timedelta(days=365)
        end_date -= timedelta(days=365)

        
    fiveYearReports=json.dumps(fiveYearReport,indent=4)
    recruiters=Recruiters.objects.filter(is_active=True)
    trainers=Trainers.objects.filter(is_active=True)
    programs=Programs.objects.filter(is_active=True)
    departments=Departments.objects.filter(is_active=True)
    response_data = {
        "statusCode":6000,
        "data":{
            "title":"Success",
            "message":"",
            "data":{
                "placedInPrograms":placedInPrograms,
                "totalPlaced":len(placedStudents),
                "recruiters":len(recruiters),
                "trainers":len(trainers),
                "programs":len(programs),
                "departments":len(departments),
                "fiveYearReports":fiveYearReports
                }
        }
    }

    return Response(response_data,status=status.HTTP_200_OK)

# ------------------------------------reports starts here-------------------------------------------#

@api_view(["GET"])
@permission_classes([AllowAny])
def students_report(request):
    
    program = request.GET.get('program')
    department = request.GET.get('department')
    
    if program:
        if Student.objects.filter(program__pk=program).exists():
            students = Student.objects.filter(program__pk=program)
    if department:
        if Student.objects.filter(program__department__pk=department).exists():
            students = Student.objects.filter(program__department__pk=department)
    if program and department:
        if Student.objects.filter(program__pk=program, program__department__pk=department).exists():
            students = Student.objects.filter(program__pk=program, program__department__pk=department)  
            
    if students:
        serializer = StudentReportSerializer(students, many=True)
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data": serializer.data,
            }
        }   
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message":"No student found."
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def student_academicDocuments(request,student_id):
    if StudentAcademicDetails.objects.filter(student_id=student_id).exists():
        docs = StudentAcademicDetails.objects.filter(student_id=student_id)
        marks = Student_program_semester.objects.filter(student_id=student_id).order_by('semester__semester__semester')
        serializer1 = StudentAcademicDocumentSerializer(docs, many=True)
        serializer2 = searchMarklisteSerialiser(marks, many=True)
        
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":serializer1.data,
                "semester_marks":serializer2.data
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def promote_student_details(request,pk):
    if Student_program_semester.objects.filter(semester__program__id=pk,semester__semester__semester='Semester 1').exists():
        students = Student_program_semester.objects.filter(semester__program__id=pk,semester__semester__semester='Semester 1',status='upcoming')
        # serializer = StudentProgramSemesterSerializer(students, many=True)
        responce_data =[]
        for student in students:
            instance ={
                "id":student.id,
                "student_name": student.student.first_name+' ' +student.student.last_name,
                "student_id": student.student.id,
                "admission_number":student.student.admission_number,
                "dob":student.student.date_of_birth.isoformat() if student.student.date_of_birth else None,
                "gender": student.student.gender,
                "roll_number":student.student.roll_number,
                "program_semester":student.semester.program.program_name+'-'+student.semester.semester.semester
            }
            responce_data.append(instance)
        responce_data_sorted = sorted(responce_data, key=lambda x: x["roll_number"])
        responce_data_sent=json.dumps(responce_data_sorted,indent=4)
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":responce_data_sent
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Success",
                "data":[],
                "message":"No Student fount"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["DELETE"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def delete_student(request):
    username = request.GET.get('username')
    student_id = request.GET.get('student_id')
    if User.objects.filter(username=username).exists() and Student.objects.filter(id=student_id).exists():
        student_to_delete =Student.objects.get(id=student_id)
        user_to_delete =User.objects.get(username=username)
        student_to_delete.delete()
        user_to_delete.delete()
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":[],
                "message":"Removed Succesfully"
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"failed",
                "data":[],
                "message":"Something went wrong! please try again"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get_recruitment_selected_students(request,pk):
    department_id = request.GET.get('department_id')
    if pk and Schedule_Recruitment.objects.filter(id=pk).exists():
        schedule_instance = Schedule_Recruitment.objects.get(id=pk)
        if Recruitment_Participated_Students.objects.filter(scheduled_recruitment=schedule_instance).exists():
            if department_id:
                department_id = int(department_id)
                participated_students = Recruitment_Participated_Students.objects.filter(scheduled_recruitment=schedule_instance,student__program__department__id=department_id)
            else:
                participated_students = Recruitment_Participated_Students.objects.filter(scheduled_recruitment=schedule_instance)
            selected_students =[]
            for instance in participated_students:
                if Placed_students.objects.filter(recruitment_participated_student=instance).exists():
                    placed_details = Placed_students.objects.filter(recruitment_participated_student=instance)
                    placed_details=placed_details[0]
                    instance_of_placed = {
                        "admission_number" : instance.student.admission_number,
                        "program" : instance.student.program.program_name,
                        "gender" : instance.student.gender,
                        "student_name" : instance.student.first_name+' '+instance.student.last_name,
                        "applied_date" : instance.applied_date.isoformat() if instance.applied_date else None,
                        "placed_date" : placed_details.placed_date.isoformat() if placed_details.placed_date else None,
                        "status" : "Qualified"
                    }
                    selected_students.append(instance_of_placed)
            responce_data_sent=json.dumps(selected_students,indent=4)
            total_applied_students = Recruitment_Participated_Students.objects.filter(scheduled_recruitment__id=pk)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"success",
                    "data":responce_data_sent,
                    "total_applied_students" : len(total_applied_students),
                    "message":"Get succesfull"
                }
            }
        else:
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"success",
                    "data":[],
                    "total_applied_students":0,
                    "message":"No Students Applied"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"failed",
                "data":[],
                "message":"Not found"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes((AllowAny,))
def constrols(request):
    if Controls.objects.all():
        departments = Controls.objects.all()  
        serializer = ControlGetSerializer(departments, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get_alumni_batch_details(request):
    if alumni_batch_details.objects.all():
        sorted_batch_details = alumni_batch_details.objects.all().order_by('-start_year', '-end_year')
        batch_details_list = [{'startyear': item.start_year, 'endyear': item.end_year} for item in sorted_batch_details]
        responce_data_sent=json.dumps(batch_details_list,indent=4)
        response_data = {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":responce_data_sent
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["POST"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def alumni_register(request):
    serializer = AlumniRegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        firstName = request.data['firstName']
        lastName = request.data['lastName']
        gender = request.data['gender']
        dateOfBirth = request.data['dateOfBirth']
        address = request.data['address']
        phone = request.data['phone']
        email = request.data['email']
        program = request.data['program']
        startYear = request.data['startYear']
        endYear = request.data['endYear']
        batch_instance, created = alumni_batch_details.objects.get_or_create(
            start_year=startYear, end_year=endYear
            )
        program_instance = Programs.objects.get(id=program)
        alumni_details.objects.create(
            first_name =firstName,
            last_name = lastName,
            date_of_birth =dateOfBirth,
            address = address,
            gender = gender,
            phone =phone,
            email = email,
            program = program_instance,
            batch = batch_instance
        )

        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Alumni Registred Succesfully",
                "data":[],
                
            }
        }  
    else: 
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Alumni Registration failed.",
                "data":[],
                "error":serializer.errors
            }
        }  
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get_alumni_details(request):
    program = request.GET.get('program')
    startYear = request.GET.get('startYear')
    endYear = request.GET.get('endYear')
    if program and startYear and endYear:
        if alumni_batch_details.objects.filter(start_year=startYear,end_year=endYear).exists():
            batch = alumni_batch_details.objects.filter(start_year=startYear,end_year=endYear)[0]
            alumniDetails = alumni_details.objects.filter(batch=batch,program_id=program).order_by('first_name')
            alumniDetailsdata=[]
            for i in alumniDetails:
                jobDetailsData= []
                if alumni_job.objects.filter(person=i).exists():
                    jobDetails = alumni_job.objects.filter(person=i).order_by('start_date')
                    for j in jobDetails:

                        jobInstance ={
                            "job_id":j.id,
                            "job_title": j.job_title,
                            "company": j.company,
                            "start_date":j.start_date.isoformat()  if j.start_date else None,
                            "end_date":j.end_date.isoformat()  if j.end_date else None
                        }
                        jobDetailsData.append(jobInstance)
                alumniInstance = {
                    "id":i.id,
                    "first_name" : i.first_name,
                    "last_name" :i.last_name,
                    "date_of_birth":i.date_of_birth.isoformat()  if i.date_of_birth else None,
                    "address" :i.address,
                    "gender" :i.gender,
                    "phone" :i.phone,
                    "email" :i.email,
                    "program" :i.program.program_name,
                    "department" :i.program.department.department_name,
                    "batch" : str(i.batch.start_year)+' '+str(i.batch.end_year),
                    # "photo" : i.photo,
                    "jobDetails" : jobDetailsData
                } 
                alumniDetailsdata.append(alumniInstance)
            responce_data_sent=json.dumps(alumniDetailsdata,indent=4)   
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":responce_data_sent,
                    "message":"Succesfull"
                }
            }
        else:
             response_data = {
            "statusCode":6001,
            "data":{
                "title":"failed",
                "data":[],
                "message":"Batch Not Exists"
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"failed",
                "data":[],
                "message":"Something went wrong! please try again"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["PUT"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def update_job_instance(request):
    job_id = request.data.get('job_id')
    end_date = request.data.get('end_date')
    if job_id and end_date:
        if alumni_job.objects.filter(id=job_id).exists():
            job_instance = alumni_job.objects.get(pk=job_id)
            job_instance.end_date=end_date
            job_instance.save()
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":[],
                    "message":"Job instance updated succesfully"
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Something went wrong. Please Try again"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"Something went wrong. Please Try again"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["POST"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def create_new_job_instance(request):
    id = request.data.get('id')
    job_title = request.data.get('job_title')
    company = request.data.get('company')
    start_date = request.data.get('start_date')
    if id and job_title and company and start_date:
        person_id = int(id)
        if alumni_details.objects.filter(id=person_id).exists():
            person = alumni_details.objects.get(id=person_id)
            alumni_job_instance = alumni_job(
                job_title=job_title,
                company=company,
                start_date=start_date,
                person=person,
            )
            alumni_job_instance.save()
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":[],
                    "message":"Job instance created succesfully"
                }
            }
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"Something went wrong. Please Try again"
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"Something went wrong. Please Try again"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["student","Admin","Placement_officer","HOD","Staff_Coordinator"])
def student_semester_marklist_details(request,student_id):
    if student_id:
        if Student.objects.filter(id=student_id).exists():
            # student = Student.objects.get(id=student_id)
            if Student_program_semester.objects.filter(student__id=student_id).exists():
                student = Student_program_semester.objects.filter(student__id=student_id,status='completed').order_by('semester__semester__semester')
                serializer = MarklistDetailsStudentSeralizer(student,many=True)
                # serializer = StudentProgramSemesterSerializer(student, many=True)
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":serializer.data,
                        "message":""
                    }
                }
            else:
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":[],
                        "message":""
                    }
                }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Student non Existing"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"No student id provided"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","student"])
def get_training_details_by_student(request,student_id):
    if student_id and Student.objects.filter(id=student_id).exists():
        student = Student.objects.get(id=student_id)
        if Student_program_semester.objects.filter(student=student).exists():
            merged_list=[]
            student_program_semesters = Student_program_semester.objects.filter(student=student).exclude(status='upcoming')
            for student_program_semester in student_program_semesters:
                if student_program_semester.start_date and student_program_semester.end_date:
                    training_participant = TrainingParticipant.objects.filter(
                        program_semester=student_program_semester.semester, 
                        allot_trainer__start_date__lte=student_program_semester.start_date,  
                        allot_trainer__end_date__gte=student_program_semester.end_date 
                        )
                elif student_program_semester.start_date:
                    training_participant = TrainingParticipant.objects.filter(
                        program_semester=student_program_semester.semester, 
                        allot_trainer__created_date__lte=student_program_semester.start_date 
                        )
                training_participant_list = list(training_participant)
                merged_list=training_participant_list+merged_list
            res_data=[]
            for training_participent in merged_list:
                focus_areas =  list(training_participent.allot_trainer.focusing_area.values_list('area_name', flat=True))
                instance ={
                    "training_id":training_participent.allot_trainer.id,
                    "trainer_name":training_participent.allot_trainer.trainer.trainer_name,
                    "start_date":training_participent.allot_trainer.start_date,
                    "end_date":training_participent.allot_trainer.end_date,
                    "venue":training_participent.allot_trainer.venue,
                    "status":training_participent.allot_trainer.status,
                    "focus_areas":focus_areas
                }
                res_data.append(instance)
            sorted_res_data = sorted(res_data, key=lambda x: x['start_date'], reverse=True)
            responce_data_sent=TrainingParticipantForStudentDetailsSerializer(sorted_res_data,many=True)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":responce_data_sent.data,
                    "message":""
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Failed to load student program details"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"No student id provided"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","student"])
def get_training_details_for_feedback_by_student(request,student_id):
    if student_id and Student.objects.filter(id=student_id).exists():
        student = Student.objects.get(id=student_id)
        if Student_program_semester.objects.filter(student=student).exists():
            merged_list=[]
            student_program_semesters = Student_program_semester.objects.filter(student=student).exclude(status='upcoming')
            for student_program_semester in student_program_semesters:
                if student_program_semester.start_date and student_program_semester.end_date:
                    training_participant = TrainingParticipant.objects.filter(
                        program_semester=student_program_semester.semester, 
                        allot_trainer__start_date__lte=student_program_semester.start_date,  
                        allot_trainer__end_date__gte=student_program_semester.end_date 
                        )
                elif student_program_semester.start_date:
                    training_participant = TrainingParticipant.objects.filter(
                        program_semester=student_program_semester.semester, 
                        allot_trainer__created_date__lte=student_program_semester.start_date 
                        )
                training_participant_list = list(training_participant)
                merged_list=training_participant_list+merged_list
            res_data=[]
            for training_participent in merged_list:
                focus_areas =  list(training_participent.allot_trainer.focusing_area.values_list('area_name', flat=True))
                instance ={
                    "training_id":training_participent.allot_trainer.id,
                    "trainer_name":training_participent.allot_trainer.trainer.trainer_name,
                    "start_date":training_participent.allot_trainer.start_date,
                    "end_date":training_participent.allot_trainer.end_date,
                    "venue":training_participent.allot_trainer.venue,
                    "status":training_participent.allot_trainer.status,
                    "focus_areas":focus_areas
                }
                res_data.append(instance)
            filtered_instances = []

            # Get the current date
            current_date = datetime.now().date()

            for instance in res_data:
                if instance["start_date"] <= current_date <= instance["end_date"]:
                    if Training_Feedback.objects.filter(date=current_date,trainer__id=instance['training_id'],student__id=student_id).exists():
                        instance['review_marked']=True
                    else:
                        instance['review_marked']=False
                    filtered_instances.append(instance)
            sorted_res_data = sorted(filtered_instances, key=lambda x: x['start_date'], reverse=True)
            responce_data_sent=TrainingReviewForStudentDetailsSerializer(sorted_res_data,many=True)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":responce_data_sent.data,
                    "message":""
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Failed to load student program details"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"No student id provided"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["POST"])
@group_required(["Admin","student"])
def post_review_for_training(request):
    trainerId = request.data.get('trainerId')
    feedback = request.data.get('feedback')
    date = request.data.get('date')
    student_id = request.data.get('student_id')
    if trainerId and feedback and date and student_id:
        id = int(trainerId)
        if AllotTrainer.objects.filter(id=id).exists():
            if Student.objects.filter(id=student_id):
                student= Student.objects.get(id=student_id)
                trainer = AllotTrainer.objects.get(id=id)
                feedback_instance = Training_Feedback(
                    review=feedback,
                    trainer=trainer,
                    date=date,
                    student=student,
                )
                feedback_instance.save()
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":[],
                        "message":"Feedback Submitted succesfully"
                    }
                }
            else:
                response_data = {
                    "statusCode":6001,
                    "data":{
                        "title":"Failed",
                        "data":[],
                        "message":"Something went wrong. Please Try again"
                    }
                }
        else:
            response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"Something went wrong. Please Try again"
            }
        }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"Something went wrong. Please Try again"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def getReviews(request):
    training_id = request.GET.get('training_id')
    date = request.GET.get('date')
    if training_id and date:
        if AllotTrainer.objects.filter(id=training_id).exists():
            if Training_Feedback.objects.filter(trainer__id=training_id,date=date).exists():
                feedback = Training_Feedback.objects.filter(trainer__id=training_id,date=date)
                serializer = TrainingFeedbackSerializer(feedback,many=True)
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":serializer.data,
                        "message":""
                    }
                }
            else:
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":[],
                        "message":""
                    }
                }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Trainer not exists"
                }
            }
    elif training_id:
        if AllotTrainer.objects.filter(id=training_id).exists():
            if Training_Feedback.objects.filter(trainer__id=training_id).exists():
                feedback = Training_Feedback.objects.filter(trainer__id=training_id)
                serializer = TrainingFeedbackSerializer(feedback,many=True)
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":serializer.data,
                        "message":""
                    }
                }
            else:
                response_data = {
                    "statusCode":6000,
                    "data":{
                        "title":"Success",
                        "data":[],
                        "message":""
                    }
                }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Trainer not exists"
                }
            }
    else:
         response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Trainer id not exists"
                }
            }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","student"])
def upload_makelist_details(request):
    try:
        student_program_semester_id = request.data.get('id')
        marklist = request.FILES.get('marklist')
        backlog_count_str = request.data.get('backlog_count')
        
        cgpa = request.data.get('cgpa')

        # Retrieve the Student_program_semester instance
        sps = Student_program_semester.objects.get(pk=student_program_semester_id)

        # Update the fields
        if marklist:
            sps.marklist = marklist
        if backlog_count_str:
            backlog_count=int(backlog_count_str)
            sps.backlog_count = backlog_count
        if cgpa:
            cgpa_float=float(cgpa)
            sps.cgpa = cgpa_float

        sps.save()

        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Marklist updated successfully.",
                "data": []
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    except :
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_uploaded_marklist_details(request):
#     filtered_objects = Student_program_semester.objects.exclude(marklist__exact='').filter(
#     Q(marklist_appove_status__isnull=True) | Q(marklist_appove_status='Rejected') )
#     distinct_combinationss = filtered_objects.values('start_date', 'end_date', 'semester__semester__semester','semester__program__program_name', 'semester').distinct()
#     serializer = DistinctCombinationsSerializer(distinct_combinationss,many=True)
#     response_data = {
#             "statusCode":6000,
#             "data":{
#                 "title":"Success",
#                 "data":serializer.data,
#                 "message":"NotFound"
#             }
#         }

#     return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get_uploaded_marklist_details(request):
    department_id = request.GET.get('department_id')
    try:
        if department_id:
            filtered_objects = Student_program_semester.objects.exclude(marklist='').order_by('-end_date').filter(
                Q(marklist_appove_status__isnull=True) | Q(marklist_appove_status='Rejected'),semester__program__department__id=department_id
            ).prefetch_related('semester__semester', 'semester__program')
        else:
            filtered_objects = Student_program_semester.objects.exclude(marklist='').order_by('-end_date').filter(
                Q(marklist_appove_status__isnull=True) | Q(marklist_appove_status='Rejected')
            ).prefetch_related('semester__semester', 'semester__program')

        distinct_combinationss = filtered_objects.values(
            'start_date',
            'end_date',
            'semester__semester__semester',
            'semester__program__program_name',
            'semester'
        ).distinct()

        serializer = DistinctCombinationsSerializer(distinct_combinationss, many=True)
        
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "data": serializer.data,
                "message": ""
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except :
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Error",
                "message": "Something went wrong",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def get__marklist_varification_details_by_stu_pro_sem(request):
    try:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        pgmSemId = request.GET.get('pgmSemId')
        pgmsem = Program_Semester.objects.get(id=pgmSemId)
        details = Student_program_semester.objects.filter(semester=pgmsem,start_date=start_date,end_date=end_date).exclude(marklist='').filter(
            Q(marklist_appove_status__isnull=True) | Q(marklist_appove_status='Rejected')
        )
        serializer = StudentProgramSemesterMarklistSerializer(details,many=True)
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "data": serializer.data,
                "message": ""
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Something went wrong",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def student_marklist_verification(request):
    try:
        student_program_semester_id = request.data.get('id')
        updateStatus = request.data.get('status')
        instance = Student_program_semester.objects.get(pk=int(student_program_semester_id))
        instance.marklist_appove_status = updateStatus
        if updateStatus=='Rejected':
            instance.marklist = None
        instance.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "data": [],
                "message": "Marklist Verified Succesfully"
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "message": "Something went wrong",
                "data":[]
            }
        }
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def student_search(request):
    search_value = request.GET.get("search_value", "")
    department_id = request.GET.get("department_id")
    if search_value:
        if department_id:
            students = Student.objects.filter(
                Q(admission_number__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                (Q(first_name__iexact=search_value.split()[0]) &
                Q(last_name__icontains=search_value.split()[-1]))
            ).filter(program__department__id=department_id)
        else:
             students = Student.objects.filter(
                Q(admission_number__icontains=search_value) |
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                (Q(first_name__iexact=search_value.split()[0]) &
                Q(last_name__icontains=search_value.split()[-1]))
            )
        serializer = StudentSerializer(students, many=True)
        dataSend=[]
        for student in students:
            semester = ''
            if Student_program_semester.objects.filter(student=student,status='ongoing').exists():
                semester=Student_program_semester.objects.filter(student=student,status='ongoing')[0].semester.semester.semester
            # if Student_Resume.objects.filter(student=student).exists():
            resumeSeralizer = searchResumeSerialiser(Student_Resume.objects.filter(student=student),many=True)
            # if Student_program_semester.objects.filter(student=student).exists():
            marklist = []
            for instance in Student_program_semester.objects.filter(student=student):
                instance_data = {
                        "id":instance.id,
                        "start_date":instance.start_date.isoformat()  if instance.start_date else None,
                        "end_date":instance.end_date.isoformat()  if instance.end_date else None,
                        "sem_status":instance.status,
                        "marklist_appove_status":instance.marklist_appove_status,
                        "marklist":instance.marklist,
                        "backlog_count":instance.backlog_count,
                        "cgpa":instance.cgpa,
                        "semester":instance.semester.semester.semester,
                    }
                marklist.append(instance_data)
            sorted_res_data = sorted(marklist, key=lambda instance: instance["semester"])
            marklistToSend = StudentMarklistSerializer(sorted_res_data,many=True)
            # if Student_Additional_Documents.objects.filter(student=student).exists():
            additionalDocumentSerialiser = searchAdditionalDocumentSerialiser(Student_Additional_Documents.objects.filter(student=student),many=True)
            studentAcademicDocumentSerializer = StudentAcademicDocumentSerializer(StudentAcademicDetails.objects.filter(student=student),many=True)
            resDataInstance={
                "admission_number" : student.admission_number,
                "first_name" : student.first_name,
                "last_name" : student.last_name,
                "date_of_birth" : student.date_of_birth.isoformat() if student.date_of_birth else None,
                "address" : student.address,
                "gender" : student.gender,
                "phone" : student.phone,
                "email" : student.email,
                "marital_status" : student.marital_status,
                "admission_year" : student.admission_year,
                "roll_number" : student.roll_number,
                "parent_name" : student.parent_name,
                "parent_phone_number" : student.parent_phone_number,
                "parent_email" : student.parent_email,
                "program" : student.program.program_name,
                "semester":semester if semester else None,
                "resume" : resumeSeralizer.data,
                "marklist" :marklistToSend.data,
                "additional" : additionalDocumentSerialiser.data,
                "studentAcademicDocuments":studentAcademicDocumentSerializer.data
            }
            dataSend.append(resDataInstance)
        responce_data_sent=json.dumps(dataSend,indent=4) 
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "data": responce_data_sent,
                "message": "Search Succesfull"
            }
        }
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "data": [],
                "message": ""
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["PUT"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def update_recruitment_participation_student(request):
    rec_stud_id = request.data.get('rec_stud_id')
    statusOfUpdation = request.data.get('status')
    if rec_stud_id and statusOfUpdation:
        if Recruitment_Participated_Students.objects.filter(id=rec_stud_id).exists():
            recruitment_instance = Recruitment_Participated_Students.objects.get(pk=rec_stud_id)
            recruitment_instance.status=statusOfUpdation
            recruitment_instance.save()
            if statusOfUpdation=='Rejected':
                if Placed_students.objects.filter(recruitment_participated_student__id=rec_stud_id).exists():
                    Placed_students.objects.filter(recruitment_participated_student__id=rec_stud_id).delete()
                if Recruitment_Student_Updations.objects.filter(recruitment_participated_student__id=rec_stud_id).exists():
                    Recruitment_Student_Updations.objects.filter(recruitment_participated_student__id=rec_stud_id).delete()
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":[],
                    "message":"Updated succesfully"
                }
            }
        else:
            response_data = {
                "statusCode":6001,
                "data":{
                    "title":"Failed",
                    "data":[],
                    "message":"Something went wrong. Please Try again"
                }
            }
    else:
        response_data = {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "data":[],
                "message":"Something went wrong. Please Try again"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def program_list_all(request):
    if Programs.objects.filter(is_active=True).exists():
        programs = Programs.objects.all().order_by('program_name')
        serializer = ProgramsGetWithDepartmentSerializer(programs, many=True)
        
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def alumni_search(request):
    search_value = request.GET.get("search_value", "")
    department_id = request.GET.get("department_id")
    if search_value:
        if department_id:
            alumni = alumni_details.objects.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                (Q(first_name__iexact=search_value.split()[0]) &
                Q(last_name__icontains=search_value.split()[-1]))
            ).filter(program__department__id=department_id)
            serializer = AlumniDetailsSerializer(alumni,many=True)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":serializer.data
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
        else:
            alumni = alumni_details.objects.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(phone__icontains=search_value) |
                (Q(first_name__iexact=search_value.split()[0]) &
                Q(last_name__icontains=search_value.split()[-1]))
            )
            serializer = AlumniDetailsSerializer(alumni,many=True)
            response_data = {
                "statusCode":6000,
                "data":{
                    "title":"Success",
                    "data":serializer.data
                }
            }
            return Response(response_data,status=status.HTTP_200_OK)
    else:
        response_data = {
            "statusCode": 6001,
            "data": {
                "title": "Failed",
                "data": [],
                "message": ""
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)
    

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator"])
def active_recruiters_list(request):
    if Recruiters.objects.filter().exists():
        recruiter = Recruiters.objects.filter(is_active=True).order_by('-id')
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)