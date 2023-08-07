from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Departments)
admin.site.register(Programs)
admin.site.register(Recruiters)
admin.site.register(Trainers)
admin.site.register(Student)
admin.site.register(Semesters)
admin.site.register(Program_Semester)
admin.site.register(AllotTrainer)
admin.site.register(FocusingArea)