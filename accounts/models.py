from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.hashers import make_password

# Create your models here.
class User(AbstractUser):

    Role_choices = (
        ('Admin', 'Admin'),
        ('Placement_officer', 'Placement officer'),
        ('HOD', 'HOD'),
        ('Staff_Coordinator', 'Staff Coordinator'),
        ('Student_cordinator','Student cordinator'),
    )

    role = models.CharField(max_length=50, choices=Role_choices, blank=True, null=True)
    department = models.ForeignKey("main.Departments", on_delete=models.CASCADE, blank=True, null=True)
    user_active=models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'Admin'
            self.department = None
        elif self.role in ['Admin', 'Placement_officer']:
            self.department = None
            
        return super(User, self).save(*args, **kwargs)