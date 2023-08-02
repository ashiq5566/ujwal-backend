# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import User
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()
    email = serializers.CharField()
    department = serializers.CharField()
    user_active = serializers.BooleanField()
