
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['POST'])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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

@api_view(["GET"])
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
def program_list(request):
    if Programs.objects.filter(is_active=True).exists():
        programs = Programs.objects.filter(is_active=True)
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
def programs_by_department(request, pk):
    if Departments.objects.get(id=pk):
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
def program_semester_by_program(request, pk):
    if Programs.objects.get(id=pk):
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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

                    
                    allot_trainer=AllotTrainer(trainer=trainer,start_date=start_date,end_date=end_date,venue=venue)
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
def training_participents_details(request):
    allot_tariner_id = request.GET.get('allot_tariner_id')
    if allot_tariner_id:
        allot_tariner_id = int(allot_tariner_id)
        training_participant = TrainingParticipant.objects.filter(allot_trainer__id=allot_tariner_id) ;  
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
        if TrainingParticipant.objects.get(id=pk):
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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
    if Schedule_Recruitment.objects.get(id=pk):
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
    if Schedule_Recruitment.objects.get(id=pk):
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
    if AllotTrainer.objects.get(id=pk):
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
    if AllotTrainer.objects.get(id=pk):
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
def get_applied_placements_by_student(request,pk):
    student_id = int(pk)
    if Recruitment_Participated_Students.objects.filter(student__id=student_id).exists():
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
                    "completed_status" :studentUpdationItem.status
                }
                updationAll.append(updationInstance)
            instance = {
                "id" : appliedPlacement.id,
                "applied_date" :  appliedPlacement.applied_date.isoformat() if appliedPlacement.applied_date else None,
                "scheduled_recruitment_id" : appliedPlacement.scheduled_recruitment.id,
                "scheduled_recruitment_name" : appliedPlacement.scheduled_recruitment.recruiter.company_name,
                "designation" : appliedPlacement.scheduled_recruitment.designation,
                "status" : appliedPlacement.scheduled_recruitment.status,
                "student_process_details":updationAll
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        student_id = request.data.get('student_id')
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator","student"])
def update_offer_latter(request):
    placed_student_id = request.data.get('placed_student_id')
    new_offer_latter = request.FILES.get('offer_latter')
    if Placed_students.objects.filter(pk=placed_student_id).exists() and request.FILES.get('offer_latter'):
        placed_student = Placed_students.objects.get(pk=placed_student_id)
        placed_student.offer_latter = new_offer_latter
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
@group_required(["Admin","Placement_officer","HOD","Staff_Coordinator","Student_cordinator"])
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

        placedInPrograms=json.dumps(pgmPlcedList,indent=4)
        fiveYearReports=json.dumps(fiveYearReport,indent=4)
    recruiters=Recruiters.objects.filter(is_active=True)
    trainers=Trainers.objects.filter(is_active=True)
    response_data = {
        "statusCode":6000,
        "data":{
            "title":"Success",
            "message":"NotFound",
            "data":{
                "placedInPrograms":placedInPrograms,
                "totalPlaced":len(placedStudents),
                "recruiters":len(recruiters),
                "trainers":len(trainers),
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