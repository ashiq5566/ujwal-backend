# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import User
from main.models import *


class DepartmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        exclude = ['department_id']

class DepartmentsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'

class TrainerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainers
        exclude = ['trainer_id']

class TrainersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainers
        fields = '__all__'

class RecruiterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiters
        exclude = ['recruiter_id']

class RecruitersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiters
        fields = '__all__'

class ProgramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        exclude = ['program_id']

class ProgramsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = '__all__'
        
        

class FocusinAreaGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusingArea
        fields = '__all__'


class SemestersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semesters
        fields = '__all__'

class ProgramSemesterGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program_Semester
        fields = '__all__'


class TrainingScheduleSerializer(serializers.Serializer):
    trainer_id = serializers.IntegerField()
    start_date_str = serializers.CharField()
    end_date_str = serializers.CharField()
    venue = serializers.CharField()
    foc_areas_ids = serializers.ListField(child=serializers.IntegerField())
    participants_ids = serializers.ListField(child=serializers.IntegerField())

class TrainingSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllotTrainer
        fields = '__all__'
    

class RecruitmentScheduleSerializer(serializers.Serializer):
    recruiter_id = serializers.IntegerField()
    date = serializers.CharField()  
    venue = serializers.CharField()
    designation = serializers.CharField()
    participants_ids = serializers.ListField(child=serializers.IntegerField())
    apply_link = serializers.URLField()
    
class RecruitmentSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule_Recruitment
        fields = '__all__'

class TrainingParticipentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingParticipant
        fields = '__all__'

class RecruitmentParticipentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Participating_Branches
        fields = '__all__'
        
        
class AttendancePostSerializer(serializers.Serializer):
    date = serializers.CharField()
    absent_student = serializers.ListField(child=serializers.IntegerField())
    present_student = serializers.ListField(child=serializers.IntegerField())
    

class StudentProgramSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_program_semester
        fields = '__all__'
        
class RecruitmentParticipatedStudentsSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Participated_Students
        fields = '__all__'
    
class RecruitmentSelectionUpdatesSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Student_Updations
        fields = '__all__'

class ParticipatedStudentsByRecruitmentSchedulesSerializer(serializers.ModelSerializer):
    participated_id = serializers.IntegerField(source='id')
    class Meta:
        model = Recruitment_Participated_Students
        fields = ['participated_id','student']


class PlacedStudentsSerializer(serializers.ModelSerializer):
    admission_number = serializers.CharField(source='recruitment_participated_student.student.admission_number')
    first_name = serializers.CharField(source='recruitment_participated_student.student.first_name')
    last_name = serializers.CharField(source='recruitment_participated_student.student.last_name')
    gender = serializers.CharField(source='recruitment_participated_student.student.gender')
    roll_number = serializers.CharField(source='recruitment_participated_student.student.roll_number')
    recruiter_company_name = serializers.CharField(source='recruitment_participated_student.scheduled_recruitment.recruiter.company_name')
    recruiter_designation = serializers.CharField(source='recruitment_participated_student.scheduled_recruitment.designation')
    program_name = serializers.CharField(source='recruitment_participated_student.student.program.program_name')
    department_name = serializers.CharField(source='recruitment_participated_student.student.program.department.department_name')
    
    class Meta:
        model = Placed_students
        fields = ['admission_number', 'first_name', 'last_name', 'gender','roll_number',
                  'recruiter_company_name', 'recruiter_designation', 'program_name', 'department_name', 'placed_date']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = '__all__'

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_year
        fields = '__all__'
