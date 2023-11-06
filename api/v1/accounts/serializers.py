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
        fields = ['first_name','last_name','email','department','user_active','username','role','password']
    
class StudentSerializer(serializers.Serializer):
    admission_number = serializers.IntegerField()
    roll_number = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    date_of_birth = serializers.CharField()
    address = serializers.CharField()
    gender = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    marital_status = serializers.CharField()
    admission_year = serializers.IntegerField()
    parent_name = serializers.CharField()
    parent_phone_number = serializers.CharField()
    parent_email = serializers.EmailField()
    program_id = serializers.IntegerField()
    username = serializers.CharField()
    password = serializers.CharField()
    # image = serializers.ImageField()
    
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        
class StudentDocumentsSerializer(serializers.Serializer):
    student = serializers.CharField()
    document_type = serializers.CharField()
    document_file = serializers.FileField()
    mark = serializers.CharField()

        
class DepartmentsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['department_name']
        
class EditUserPassword(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
        