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
    re_path(r"^edit-password/$", edit_password),
    re_path(r"^control_user/$", control_user),
    
    #studentside
    re_path(r"^students/register/$", student_register),
    re_path(r"^students/register_with_documents/$", student_register_with_documents),
    re_path(r"^students/document_upload/$", student_document_upload),
    re_path(r"^students/documents/$", student_documents),
    re_path(r"^students/documents/(?P<pk>\d+)/$", student_document_details),
    re_path(r"^students/$", students),
    re_path(r"^students/(?P<pk>\d+)/$", student_details),
    


    #toke generation using jwt
    re_path(r"^token/$", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    re_path(r"^token/refresh/$", TokenRefreshView.as_view(), name="token_refresh"),

    
]