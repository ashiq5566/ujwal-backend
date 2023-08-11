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
    
admin.site.register(Departments,DepartmentsAdmin)
admin.site.register(Programs,ProgramsAdmin)
admin.site.register(Recruiters)
admin.site.register(Trainers)
admin.site.register(Student, StudentAdmin)
admin.site.register(Semesters)
admin.site.register(Program_Semester)
admin.site.register(AllotTrainer)
admin.site.register(FocusingArea)
admin.site.register(Schedule_Recruitment)
admin.site.register(Recruitment_Participating_Branches)
admin.site.register(StudentDocument)
admin.site.register(TrainingParticipant)