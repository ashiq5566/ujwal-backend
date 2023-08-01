import json
import requests

# from pprint import pprint


from accounts.models import User


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