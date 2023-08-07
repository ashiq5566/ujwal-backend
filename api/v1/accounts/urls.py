from django.urls import path, re_path


from .views import  *
urlpatterns = [
    #student_side
    re_path(r"^login/$", login),
    re_path(r"^register/$", user_register),
    re_path(r"^users/$", user_list),
]