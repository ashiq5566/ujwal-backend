from django.contrib import admin
from accounts.models import User
from main.models import *


admin.site.site_header="Ujwal Administration Panel"

# Register your models here.
admin.site.register(User)
admin.site.register(Departments)
admin.site.register(Programs)
admin.site.register(Recruiters)
admin.site.register(Trainers)
admin.site.register(Student)

