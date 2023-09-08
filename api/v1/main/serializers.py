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
    number_of_hirings = serializers.IntegerField()
    apply_last_date = serializers.CharField() 
    description =  serializers.CharField() 
    

class RecruitmentSchedulesSerializer(serializers.ModelSerializer):
    participents_details = serializers.SerializerMethodField()
    recruiter_name =serializers.CharField(source='recruiter.company_name')

    class Meta:
        model = Schedule_Recruitment
        fields = '__all__'

    def get_participents_details(self, obj):
        schedule_id = obj.id
        filtered_data = Recruitment_Participating_Branches.objects.filter(scheduled_recruitment_id=schedule_id)
        serialized_data = RecruitmentParticipentsSerializer(filtered_data, many=True).data
        return serialized_data

class TrainingParticipentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingParticipant
        fields = '__all__'

class RecruitmentParticipentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Participating_Branches
        fields = '__all__'

class RecruitmentParticipentsSerializer(serializers.ModelSerializer):
    program_semester = serializers.SerializerMethodField()
    class Meta:
        model = Recruitment_Participating_Branches
        fields = ['scheduled_recruitment','program_semester']

    def get_program_semester(self, obj):
        program_semesters = obj.program_semester.all()  # Assuming you want to retrieve all related Program_Semester instances
        serialized_program_semesters = []  # List to store serialized Program_Semester data
        for program_semester in program_semesters:
            serialized_program_semester = {
                'program_semester': program_semester.id,  # You can customize the fields you want to include
                'program': program_semester.program.id,  # You can customize the fields you want to include
                'program_name': program_semester.program.program_name,  # You can customize the fields you want to include
                'semester': program_semester.semester.id,
                'semester_name': program_semester.semester.semester,
            }
            serialized_program_semesters.append(serialized_program_semester)
        return serialized_program_semesters       
        
class AttendancePostSerializer(serializers.Serializer):
    date = serializers.CharField()
    absent_student = serializers.ListField(child=serializers.IntegerField())
    present_student = serializers.ListField(child=serializers.IntegerField())
    

class StudentProgramSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_program_semester
        fields = '__all__'
        
class RecruitmentParticipatedStudentsSchedulesSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='student.program.program_name')
    program_name = serializers.CharField(source='student.program.department.department_name')
    admission_number = serializers.CharField(source='student.admission_number')
    first_name = serializers.CharField(source='student.first_name')
    last_name = serializers.CharField(source='student.last_name')
    gender = serializers.CharField(source='student.gender')
    roll_number = serializers.CharField(source='student.roll_number')
    designation = serializers.CharField(source='scheduled_recruitment.designation')
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
