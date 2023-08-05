# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import User
from main.models import *
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

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