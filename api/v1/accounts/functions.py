import json
import requests
from django.conf import settings
from cryptography.fernet import Fernet
import base64
from accounts.models import User




def encrypt(text):
    text = str(text)
    f = Fernet(settings.ENCRYPT_KEY)
    #input should be in bytes
    encrypted_data = f.encrypt(text.encode('ascii'))
    encrypted_data = base64.urlsafe_b64encode(encrypted_data).decode("ascii") 

    return encrypted_data


def decrypt(text):
    text= base64.urlsafe_b64decode(text)
    f = Fernet(settings.ENCRYPT_KEY)
    decrypted_data = f.decrypt(text).decode("ascii")

    return decrypted_data


def authenticate(username: str, password: str, request):

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        'grant_type': 'password',
        "username": username,
        "password": password,
    }
    protocol = "http://"
    if request.is_secure():
        protocol = "https://"

    web_host = request.get_host()
    url = protocol + web_host + "/api/v1/accounts/token/"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    user: User = User.objects.filter(username=username).latest("date_joined")
    
    if user.check_password(password):
        print("password is ok")
    
    if response.status_code == 200:
       
        return {
            "statusCode":6000,
            "data":{
                "title":"Success",
                "data":{
                    "id":user.id,
                    "username":user.username,
                    "role":user.role,
                    "email":user.email

                },
                "refresh": response.json().get("refresh"),
                "access": response.json().get("access"),
            }       
        }
    return {
            "statusCode":6001,
            "data":{
                "title":"Failed",
                "message": "Token generation failed"
            }       
        }