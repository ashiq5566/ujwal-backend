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
        