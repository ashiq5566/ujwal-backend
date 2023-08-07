from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import  *
urlpatterns = [
    #user_side
    re_path(r"^login/$", login),
    re_path(r"^register/$", user_register),
    re_path(r"^users/$", user_list),


    #toke generation using jwt
    re_path(r"^token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),
]