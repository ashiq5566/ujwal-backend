from django.contrib import admin
from accounts.models import User
from main.models import Departments

# Register your models here.
admin.site.register(User)
admin.site.register(Departments)

