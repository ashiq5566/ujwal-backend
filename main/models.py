from django.db import models


class Departments(models.Model):
    department_id = models.CharField(max_length=10,unique=True, null=False)
    department_name = models.CharField(max_length=50,null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.department_name

    def pre_save(self):
        if not self.department_id:
            last_department = Departments.objects.order_by('-department_id').first()
            if last_department:
                code = int(last_department.department_id[1:]) + 1
                self.department_id = f'D{code:02}'
            else:
                self.department_id = 'D01'

    def save(self, *args, **kwargs):
        self.pre_save()
        super(Departments, self).save(*args, **kwargs)

        if not self.is_active:
            programs = Programs.objects.filter(department=self)
            programs.update(is_active=False)
            
class Programs(models.Model):
    program_id = models.CharField(max_length=10, unique=True, null=False)
    program_name = models.CharField(max_length=50, null=False)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=False)
    number_of_semester = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.program_name
    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate ID for new instances
            last_instance = Programs.objects.last()
            if last_instance:
                last_id = int(last_instance.program_id[2:])
                self.program_id = f'TA{last_id + 1}'
            else:
                self.program_id = 'TA1'
        super().save(*args, **kwargs)

