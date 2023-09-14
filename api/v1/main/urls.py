from django.urls import path, re_path

from .views import  *


urlpatterns = [
    #departement
    re_path(r"^departments/$", department_list),
    re_path(r"^department/(?P<pk>\d+)/$", get_department_instance),
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
    re_path(r"^cancel_training_schedule/(?P<pk>\d+)/$", cancel_training_schedule_status),
    re_path(r"^complete_training_schedule/(?P<pk>\d+)/$", complete_training_schedule_status),
    
    #recruitment
    re_path(r"^recruitment/add_schedule/$", add_recruitment_schedule),
    re_path(r"^recruitment/schedules/$", recruitment_schedule),
    re_path(r"^recruitment/schedules/(?P<pk>\d+)/$", recruitment_schedule_detail), 
    re_path(r"^recruitment_participents/$", recruitment_participents_details), 
    re_path(r"^recruitment_participated_students_by_recruitment_schedule/(?P<pk>\d+)/$", recruitment_applied_students_by_recruitment_schedule),  
    re_path(r"^add_recruitment_Participated_Student/$", add_recruitment_Participated_Students),
    re_path(r"^recruitment_Student_UpdationDetails_by_Participated_Student/(?P<pk>\d+)/$", recruitment_Student_UpdationDetails_by_Participated_Student),  
    re_path(r"^recruitment_Student_UpdationDetails_by_List_of_Student/$", recruitment_Student_UpdationDetails_by_List_of_Student),
    re_path(r"^add_selection_update_for_student/$", add_selection_update_for_student),
    re_path(r"^cancel_recruitment_schedule/(?P<pk>\d+)/$", cancel_recruitment_schedule_status),
    re_path(r"^complete_recruitment_schedule/(?P<pk>\d+)/$", complete_recruitment_schedule_status),

    
    # attendance
    re_path(r"^training/add_attendance/(?P<pk>\d+)/$", attendance),
    # re_path(r"^check_Attendance_Marked_details_from_allot_trainer/(?P<pk>\d+)/$", check_Attendance_Marked_details_from_allot_trainer),
    # re_path(r'^update_attendance_marked/$', update_attendance_marked),
    re_path(r"^attendenceMarkedOrNot/$", attendenceMarkedOrNot),
    re_path(r"^getAttendence/$", getAttendence),

    #student program semester
    re_path(r"^student_program_semester_details/$", student_program_semester_details),
    re_path(r"^student_program_semester_by_program_semester/(?P<pk>\d+)/$", student_program_semester_by_program_semester),
    re_path(r"^ongoing_program_semester_promote_details/$", ongoing_program_semester_promote_details),

    #placement
    re_path(r"^get_participatedStudents_for_placement_by_schedule/(?P<pk>\d+)/$", get_participatedStudents_for_placement_by_schedule),
    re_path(r"^add_a_placement/$", add_a_placement),
    re_path(r"^get_placedStudents_by_batch/$", get_placedStudents_by_batch),


    #promote program
    re_path(r"^promote_current_batch/(?P<pk>\d+)/$",promote_current_batch),
    re_path(r"^promote_new_batch/(?P<pk>\d+)/$",promote_new_batch),

    #academic year
    re_path(r"get_academic_years/$", get_academic_years),

    #skill
    re_path(r"getSkillSetByStudent/(?P<pk>\d+)/$", getSkillSetByStudent),
    re_path(r"add_skillset/$", add_skillset),
    
    #student login
    re_path(r"get_placement_details_by_student/(?P<pk>\d+)/$", get_placement_details_by_student),
    re_path(r"get_applied_placements_by_student/(?P<pk>\d+)/$", get_applied_placements_by_student),
    re_path(r"get_placed_result_by_student/(?P<pk>\d+)/$", get_placed_result_by_student),

]