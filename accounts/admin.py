from django.contrib import admin
from accounts.models import User
from main.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Departments)
admin.site.register(Programs)
admin.site.register(Recruiters)
admin.site.register(Trainers)

