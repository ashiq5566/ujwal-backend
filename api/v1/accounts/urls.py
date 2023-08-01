from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import  login

urlpatterns = [
    #student_side
    re_path(r"^login/$", login),
 
    re_path(r"^token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),
]