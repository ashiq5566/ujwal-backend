from django.contrib import admin
from accounts.models import User
from main.models import *


admin.site.site_header="Ujwal Administration Panel"

# Register your models here.
admin.site.register(User)

