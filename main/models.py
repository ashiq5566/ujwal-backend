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


class Recruiters(models.Model):
    recruiter_id = models.CharField(max_length=10,unique=True, null=False)
    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    website = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name

    def company_save(self):
        if not self.recruiter_id:
            last_company = Recruiters.objects.order_by('-recruiter_id').first()
            print(last_company,"Last company")
            if last_company:
                code = int(last_company.recruiter_id[1:]) + 1
                self.recruiter_id = f'C{code:02}'
            else:
                self.recruiter_id = 'C01'
    
    def save(self, *args, **kwargs):
        self.company_save()
        super().save(*args, **kwargs)
    

class Trainers(models.Model):
    trainer_id = models.CharField(max_length=10,unique=True, null=False)
    trainer_name = models.CharField(max_length=100, null=False)
    training_company = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    website = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.trainer_name} - company:{self.training_company}"
    
    def trainer_save(self):
        if not self.trainer_id:
            last_trainer = Trainers.objects.order_by('-trainer_id').first()
            if last_trainer:
                code = int(last_trainer.trainer_id[1:]) + 1
                self.trainer_id = f'T{code:02}'
            else:
                self.trainer_id = 'T01'
    
    def save(self, *args, **kwargs):
        self.trainer_save()
        super().save(*args, **kwargs)

