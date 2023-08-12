from django.urls import path, re_path

from .views import  *


urlpatterns = [
    #departement
    re_path(r"^departments/$", department_list),
    re_path(r"^create_department/$", create_department),
    
    #trainer
    re_path(r"^add_trainer/$", add_trainer),
    re_path(r"^trainers/$", trainers_list),
    
    #recruiter
    re_path(r"^add_recruiter/$", add_recruiter),
    re_path(r"^recruiters/$", recruiters_list),
    
    #program
    re_path(r"^add_program/$", add_program),
    re_path(r'^update_programs/(?P<program_id>\d+)/$', update_program),
    re_path(r"^programs/$", program_list),
    re_path(r'^programs_by_department/(?P<pk>\d+)/$',programs_by_department),
    re_path(r"^semesters/$", semesters),
    re_path(r'^program_semester_by_program/(?P<pk>\d+)/$',program_semester_by_program),
    re_path(r"^program_semesters/$", program_semesters),
    
    #training
    re_path(r"^training/add_schedule/$", add_training_schedule),
    re_path(r"^training/schedules/$", training_schedule),
    re_path(r"^training/schedules/(?P<pk>\d+)/$", training_schedule_detail),
    re_path(r"^focusing_areas/$", focusing_areas),
    re_path(r"^training_participents/$", training_participents_details),
    
    #recruitment
    re_path(r"^recruitment/add_schedule/$", add_recruitment_schedule),
    re_path(r"^recruitment/schedules/$", recruitment_schedule),
    re_path(r"^recruitment/schedules/(?P<pk>\d+)/$", recruitment_schedule_detail), 
    re_path(r"^recruitment_participents/$", recruitment_participents_details),  
    
    # attendance
    re_path(r"^training/add_attendance/(?P<pk>\d+)/$", attendance),
]