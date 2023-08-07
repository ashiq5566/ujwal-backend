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