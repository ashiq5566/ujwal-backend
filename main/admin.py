from django.contrib import admin
from .models import *

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    list_display = (
    'student_id',
    'admission_number',
    'first_name',
    'last_name',
    'date_of_birth',
    'address',
    'gender',
    'phone',
    'email',
    'marital_status',
    'admission_year',
    'roll_number',
    'parent_name',
    'parent_phone_number',
    'parent_email',
    'program'
)
    
class DepartmentsAdmin(admin.ModelAdmin):
        list_display = ('department_id','department_name','is_active',)
        
        
class ProgramsAdmin(admin.ModelAdmin):
    list_display = (
    'program_id',
    'program_name',
    'department',
    'number_of_semester',
    'is_active',)
    
    
   
class AllotTrainerAdmin(admin.ModelAdmin):
    list_display = (
    'allotment_id',
    'trainer',
    'start_date',
    'end_date',
    'venue',
    'display_focusing_area',
    )
    def display_focusing_area(self, obj):
        return ", ".join(str(area) for area in obj.focusing_area.all())
    display_focusing_area.short_description = 'Focusing Areas'
 
class AttendenceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'training_participant',
        'date',
        'display_present_students',
        'display_absent_students',
    )

    def display_present_students(self, obj):
        return ", ".join([student.first_name for student in obj.present_students.all()])

    display_present_students.short_description = 'Present Students'

    def display_absent_students(self, obj):
        return ", ".join([student.first_name for student in obj.absent_student.all()])

    display_absent_students.short_description = 'Absent Students'   

admin.site.register(Attendence,AttendenceAdmin)
admin.site.register(AllotTrainer, AllotTrainerAdmin) 
admin.site.register(Departments,DepartmentsAdmin)
admin.site.register(Programs,ProgramsAdmin)
admin.site.register(Recruiters)
admin.site.register(Trainers)
admin.site.register(Student, StudentAdmin)
admin.site.register(Semesters)
admin.site.register(Program_Semester)
admin.site.register(FocusingArea)
admin.site.register(Schedule_Recruitment)
admin.site.register(Recruitment_Participating_Branches)
admin.site.register(StudentDocument)
admin.site.register(TrainingParticipant)
admin.site.register(Student_program_semester)
admin.site.register(Recruitment_Participated_Students)
admin.site.register(Recruitment_Student_Updations)
admin.site.register(CheckAttendanceMarked)
