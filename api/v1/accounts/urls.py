from django.urls import path, re_path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import  *
urlpatterns = [
    #student_side
    re_path(r"^login/$", login),
    re_path(r"^register/$", user_register),
    re_path(r"^users/$", user_list),
    re_path(r"^departments/$", department_list),
    re_path(r"^create_department/$", create_department),
    re_path(r"^users/(?P<pk>.*)/$", user_details),
    re_path(r"^add_trainer/$", add_trainer),
    re_path(r"^trainers/$", trainers_list),
    re_path(r"^add_recruiter/$", add_recruiter),
    re_path(r"^recruiters/$", recruiters_list),
    re_path(r"^add_program/$", add_program),
    re_path(r"^programs/$", program_list),

 
    re_path(r"^token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),
]