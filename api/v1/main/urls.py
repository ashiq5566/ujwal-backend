from django.urls import path, re_path

from .views import  *


urlpatterns = [
    re_path(r"^departments/$", department_list),
    re_path(r"^create_department/$", create_department),
    re_path(r"^add_trainer/$", add_trainer),
    re_path(r"^trainers/$", trainers_list),
    re_path(r"^add_recruiter/$", add_recruiter),
    re_path(r"^recruiters/$", recruiters_list),
    re_path(r"^add_program/$", add_program),
    re_path(r'^update_programs/(?P<program_id>\d+)/$', update_program),
    re_path(r"^programs/$", program_list),
    re_path(r"^focusing_areas/$", focusing_areas),
    re_path(r'^programs_by_department/(?P<pk>\d+)/$',programs_by_department),
    re_path(r"^semesters/$", semesters),
    re_path(r'^program_semester_by_program/(?P<pk>\d+)/$',program_semester_by_program),
    re_path(r"^program_semesters/$", program_semesters),
]