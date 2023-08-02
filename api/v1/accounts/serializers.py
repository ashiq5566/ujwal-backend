# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import User
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # username = serializers.CharField()
    # role = serializers.CharField()
    # email = serializers.CharField()
    # role = serializers.CharField()
    
    class Meta:
        model = User
        fields = '__all__'