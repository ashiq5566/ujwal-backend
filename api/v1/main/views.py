
import requests
import json
from django.contrib.auth.models import Group

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view

from datetime import timedelta, datetime

from .serializers import *
from api.v1.accounts.functions import authenticate
from accounts.models import User
from main.models import *

from django.db.models import Q


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


@api_view(["GET"])
@permission_classes([AllowAny])
def focusing_areas(request):
    if FocusingArea.objects.all():
        focusingArea = FocusingArea.objects.all()  
        print(focusingArea)
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
                "data":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def programs_by_department(request, pk):
    if Departments.objects.get(id=pk):
        department = Departments.objects.get(id=pk)
        program=Programs.objects.filter(department=department)
        print("sdsd",program)
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
                "data":"NotFound"
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
                "data":"NotFound"
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
                "data":"NotFound"
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
                "data":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny,])
def add_training_schedule(request):
    print(request.data,"request.data")
    serializer = TrainingScheduleSerializer(data=request.data)
    if serializer.is_valid():
        print("validationg serializer")
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
                            'message' : "Participants Not Found"
                        }
                    }
            else:
                response_data = {
                    'statusCode' : 6001,
                    'data' : {
                        'title': 'failed',
                        'message' : "Trainer Not Found"
                    }
                } 
        else:
            response_data = {
                'statusCode' : 6001,
                'data' : {
                    'title': 'failed',
                    'message' : "Focusing Area Not Found"
                }
            }
    else:
         response_data = {
            "statusCode": 6001,
            "title": "Validation Error",
            "message": serializer._errors
        }
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny,])
def training_schedule(request):
    if AllotTrainer.objects.all():
        schedule = AllotTrainer.objects.all()   
        serializer = TrainingSchedulesSerializer(schedule, many=True)
        
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
                "data":"Schedule Not Found"
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
                "data":"Schedule Not Found"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([AllowAny,])
def add_recruitment_schedule(request):
    print(request.data,"request.data")
    serializer = RecruitmentScheduleSerializer(data=request.data)
    
    if serializer.is_valid():
        print("validationg serializer")
        recruiter_id = request.data['recruiter_id']
        date_str = request.data['date']  
        venue = request.data['venue']
        designation = request.data['designation']
        participants_ids = request.data['participants_ids']
        apply_link = request.data['apply_link']
        
        if Recruiters.objects.filter(id=recruiter_id).exists():
            recruiter = Recruiters.objects.get(id=recruiter_id)
            if Program_Semester.objects.filter(id__in=participants_ids).exists():
                participants = Program_Semester.objects.filter(id__in=participants_ids)
                date = datetime.strptime(date_str, '%d-%m-%Y').strftime('%Y-%m-%d')
                
                allot_recruiter = Schedule_Recruitment(recruiter=recruiter,
                    date=date,
                    venue=venue,
                    designation=designation,
                    apply_link=apply_link
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
                    'message' : "Participants Not Found"
                }
            }
        else:
            response_data = {
                'statusCode' : 6001,
                'data' : {
                    'title': 'failed',
                    'message' : "Recruiter Not Found"
                }
            }
    else:
         response_data = {
            "statusCode": 6001,
            "title": "Validation Error",
            "message": serializer._errors
        }
    return Response(response_data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_schedule(request):
    if Schedule_Recruitment.objects.all():
        schedule = Schedule_Recruitment.objects.all()   
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
                "data":"Schedule Not Found"
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
                "data":"Schedule Not Found"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def training_participents_details(request):
    if TrainingParticipant.objects.all():
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
                "data":"NotFound"
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
                "data":"NotFound"
            }
        }

    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny,])
def attendance(request, pk):
    serializer = AttendanceSerializer(data=request.data)
    
    if serializer.is_valid():
        
        if AllotTrainer.objects.filter(id=pk).exists():
            schedules = AllotTrainer.objects.filter(id=pk)
            if TrainingParticipant.objects.filter(allot_trainer=pk).exists():
                participaing_depts = TrainingParticipant.objects.filter(allot_trainer=pk).values('program_semester')
                participants = participaing_depts.values_list('program_semester', flat=True)
                
                sd = schedules.values('start_date')
                ed = schedules.values('end_date')
                start_date = sd[0]['start_date']
                end_date = ed[0]['end_date']
                
                date_list = []
                current_date = start_date
                while current_date <= end_date:
                    date_list.append(current_date)
                    current_date += timedelta(days=1)
                    
                student_sems_list = []
                for each in participants:
                    if Program_Semester.objects.get(id=each):
                        pgm_sem = Program_Semester.objects.get(id=each)
                        if Student_program_semester.objects.filter(semester=pgm_sem,status="ongoing").exists():
                            student_list = Student_program_semester.objects.filter(semester=pgm_sem,status="ongoing").values('id')
                            student_sems = list(student_list.values_list('id', flat=True))
                            student_sems_list.extend(student_sems)
                            
                        else:
                            response_data = {
                                "statusCode": 6001,
                                "title": "Failed",
                                "message": "Student List not Found"
                            }
                            
                    else:
                        response_data = {
                            "statusCode": 6001,
                            "title": "Failed",
                            "message": "Program semester not Found"
                        }
                
                students = Student_program_semester.objects.filter(id__in=student_sems_list).values('student_id')
                students_list = list(students.values_list('student_id', flat=True))
                student_s = Student.objects.filter(id__in=students_list)
                all_students = [str(student.id) for student in student_s]# Get a list of all student IDs
                participant_id = TrainingParticipant.objects.filter(allot_trainer=pk).values('id')
                participants_id_list = participant_id.values_list('id', flat=True)
                training_p = TrainingParticipant.objects.all()
                
                absent_students = request.data['absent_student']
                present_student = request.data['present_student']
                date1 = request.data['date']
                absent_studs = list(Student.objects.filter(id__in=absent_students).values_list('id', flat=True))
                for each in participants_id_list:
                    attendence = Attendence(training_participant=training_p.get(id=each),date=date1)
                    attendence.save()
                    a = TrainingParticipant.objects.filter(id=each).values('program_semester')
                    b = Student_program_semester.objects.filter(semester__in=a).values('student')
                    c = Student.objects.filter(id__in=b).values_list('id', flat=True)
                    absent = [id for id in absent_students if id in c]
                    present = [id for id in c if id in present_student]
                    attendence.absent_student.set(absent)
                    attendence.present_students.set(present)
                
                response_data = {
                    "statusCode": 6000,
                    "title": "Success",
                    "message": "Attendence Added SuccessFully"
                }
            else:
                response_data = {
                    "statusCode": 6001,
                    "title": "Failed",
                    "message": "TrainingParticipant not Found"
                }
                
        else:
            response_data = {
                "statusCode": 6001,
                "title": "Failed",
                "message": "Schedule not Found"
            }
        
    else:
        response_data = {
        "statusCode": 6001,
        "title": "Validation Error",
        "message": serializer._errors
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
                    "data":"NotFound"
                }
            }    
    return Response(response_data,status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny,])
def recruitment_applied_students_by_recruitment_schedule(request, pk):
    if Recruitment_Participated_Students.objects.filter(scheduled_recruitment_id=pk).exists():
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
                "data":"Participated student list Not Found"
            }
        }
    return Response(response_data,status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny,])
def student_program_semester_by_program_semester(request, pk):
    if Program_Semester.objects.filter(id=pk).exists():
        students_program_semester =Student_program_semester.objects.filter(semester_id=pk)
        print(students_program_semester,pk,"pk")
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
                "data":"Program semester Not Found"
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
            "errors": serializer.errors
        }
    }
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)