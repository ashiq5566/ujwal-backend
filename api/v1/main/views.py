
import requests
import json
from django.contrib.auth.models import Group

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
                "data":[],
                "message":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
                "data":[],
                "message":"NotFound"
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
            "errors": serializer.errors,
            "data":[]
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
                "data":[],
                "message":"NotFound"
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
            "errors": serializer.errors,
            "data":[]
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
                "data":[],
                "message":"NotFound"
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
                    "start_date":allot_trainer.start_date.isoformat(),
                    "end_date":allot_trainer.end_date.isoformat(),
                    "status":allot_trainer.status
                    }
                pgmSems=[]
                departmentCheck=False
                for training_participant in allot_trainer.trainingparticipant_set.all():
                    # print(training_participant.program_semester.program.department.id,"sfd",department_id,"department_id")
                    # print(f"Training Participant Department ID: {repr(training_participant.program_semester.program.department.id)}")
                    department_id = int(department_id)
                    if training_participant.program_semester.program.department.id == department_id:
                        departmentCheck=True
                        print("cheking")
                    print(departmentCheck,"departmentCheck")
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
                    "start_date":allot_trainer.start_date.isoformat(),
                    "end_date":allot_trainer.end_date.isoformat(),
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
@permission_classes([AllowAny])
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
    elif TrainingParticipant.objects.filter(allot_trainer__id=pk):
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def add_recruitment_Participated_Students(request):
    serializer = RecruitmentParticipatedStudentsSchedulesSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "statusCode": 6000,
            "data": {
                "title": "Success",
                "message": "Recruitment participatindg student added successfully."
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def ongoing_program_semester_promote_details(request):
    department_id = request.GET.get('department_id')
    if department_id:
        ongoing_semester_ids = list(set([i.semester.id for i in Student_program_semester.objects.filter(status='ongoing')]))
        print(ongoing_semester_ids,"ongoing_semester_ids")
        
        upcoming_new_sem_ids=[]
        for i in Student_program_semester.objects.filter(status='upcoming'):
            for j in Program_Semester.objects.filter(id=i.semester.id):
                sem_1=Semesters.objects.get(semester="Semester 1")
                if j.semester.id==sem_1.id:
                    upcoming_new_sem_ids += [i.semester.id]
                    print()
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
        print(ongoing_semester_ids,"ongoing_semester_ids")
        
        upcoming_new_sem_ids=[]
        for i in Student_program_semester.objects.filter(status='upcoming'):
            for j in Program_Semester.objects.filter(id=i.semester.id):
                sem_1=Semesters.objects.get(semester="Semester 1")
                if j.semester.id==sem_1.id:
                    upcoming_new_sem_ids += [i.semester.id]
                    print()
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def add_a_placement(request):
    serializer = PlacedStudentsSerializer(data=request.data)
    
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def getSkillSetByStudent(request,pk):
    if Student_skills.objects.filter(student__id=pk).exists():
        skill = Student_skills.objects.filter(student__id=pk)
        data = []  
        for i in skill:
            print(i,"sfdsdf")
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
@permission_classes([AllowAny])
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