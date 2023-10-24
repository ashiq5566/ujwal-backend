from django.contrib.auth.models import Group
from django.db import models
from api.v1.accounts.functions import encrypt, decrypt
from accounts.models import User
from datetime import timedelta ,datetime


DOCUMENT_TYPE_CHOICES = [
    ('sslc', 'SSLC'),
    ('cv', 'CV'),
    ('plus_two', 'Plus Two Certificate'),
    ('degree_certificate', 'Degree Certificate'),
    ('experience_certificate', 'Experience Certificate'),
]

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
    TYPE_CHOICES = (
        ('UG', 'UG'),
        ('PG Engineering', 'PG Engineering'),
        ('PG', 'PG'),
    )
    program_id = models.CharField(max_length=10, unique=True, null=False)
    program_name = models.CharField(max_length=100, null=False)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=50,null=True,blank=True,choices=TYPE_CHOICES)
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
    website = models.URLField(null=True,blank=True)
    contact_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name

    def company_save(self):
        if not self.recruiter_id:
            last_company = Recruiters.objects.order_by('-recruiter_id').first()
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
    website = models.CharField(max_length=150)
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

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=10,unique=True, null=False)
    admission_number = models.CharField(max_length=10, unique=True, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.TextField()
    gender = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, null=False)
    email = models.EmailField(null=False)
    marital_status = models.CharField(max_length=15)
    admission_year = models.IntegerField(null=False)
    roll_number = models.CharField(max_length=10, null=True,blank=True)
    parent_name = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=15,unique=False)
    parent_email = models.EmailField()
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, null=True,blank=True)
    password = models.CharField(blank=True, null=True)
    # image = models.ImageField(upload_to='students/', null=True, blank=True)
    

    def __str__(self):
        return f"{self.admission_number}-{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            last_student = Student.objects.order_by('-student_id').first()
            if last_student:
                code = int(last_student.student_id[1:]) + 1
                self.student_id = f'S{code:02}'
            else:
                self.student_id = 'S01'
        
        if self._state.adding:
            username = self.username
            password = self.password

            user = User.objects.create_user(username=username, password=password, role="student", email=self.email,is_active=False)
            self.password = encrypt(password)
            
            s_group, created = Group.objects.get_or_create(
                name="student"
            )
            user.role = "student"
            s_group.user_set.add(user)
            self.user = user
        
        super().save(*args, **kwargs)

class StudentAcademicDetails(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    SSLC_Mark = models.FloatField(max_length=50)
    SSLC_Document = models.FileField(upload_to='student_documents/sslc/')
    Plus_Two_Mark = models.FloatField(max_length=50)
    Plus_Two_Document = models.FileField(upload_to='student_documents/plusTwo/')
    Degree_Mark = models.FloatField(max_length=50,null=True,blank=True)
    Degree_Document = models.FileField(upload_to='student_documents/degree/',null=True,blank=True)
    Engineering_Mark = models.FloatField(max_length=50,null=True,blank=True)
    Engineering_Document = models.FileField(upload_to='student_documents/engineering/',null=True,blank=True)

    def __str__(self):
        return f"{self.student}"

class Semesters(models.Model):
    semester = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.semester
    
class Program_Semester(models.Model):
    program = models.ForeignKey("main.Programs",on_delete=models.CASCADE)
    semester = models.ForeignKey("main.Semesters",on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.program}-{self.semester}" 
    
class Student_program_semester(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('upcoming', 'Upcoming'),
    )
    APPROVED_CHOICES = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    )
    student = models.ForeignKey("main.Student",on_delete=models.CASCADE)
    semester = models.ForeignKey("main.Program_Semester",on_delete=models.CASCADE)
    start_date = models.DateField(null=True,blank=True) 
    end_date = models.DateField(null=True,blank=True)     
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='upcoming')
    marklist_appove_status = models.CharField(max_length=20, choices=APPROVED_CHOICES,null=True,blank=True)
    marklist = models.ImageField(upload_to='student_documents/marklist/', null=True,blank=True)
    backlog_count = models.PositiveSmallIntegerField(null=True,blank=True)
    cgpa=models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return f"{self.student},{self.semester},{self.status}"
    
class FocusingArea(models.Model):
    area_name = models.CharField(max_length=100)

    def __str__(self):
        return self.area_name  

    
       
class AllotTrainer(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('cancelled', 'Cancelled'),
    )
    allotment_id = models.CharField(max_length=10, unique=True, null=False)
    trainer = models.ForeignKey(Trainers, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    venue = models.CharField(max_length=100)
    focusing_area = models.ManyToManyField(FocusingArea)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='ongoing')
    created_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.trainer}"
    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate ID for new instances
            last_instance = AllotTrainer.objects.last()
            if last_instance:
                last_id = int(last_instance.allotment_id[2:])
                self.allotment_id = f'TA{last_id + 1}'
            else:
                self.allotment_id = 'TA1'

        super().save(*args, **kwargs)



class TrainingParticipant(models.Model):
    allot_trainer = models.ForeignKey(AllotTrainer, on_delete=models.CASCADE)
    program_semester = models.ForeignKey(Program_Semester,on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.allot_trainer} - {self.program_semester}"   
  


class Schedule_Recruitment(models.Model):
    STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('ongoing', 'Ongoing'),
        ('cancelled', 'Cancelled'),
    )
    recruiter = models.ForeignKey(Recruiters,on_delete=models.CASCADE, null=False)
    venue = models.CharField(max_length=50, null=True,blank=True)
    designation=models.CharField(max_length=50)
    date=models.DateField(null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='ongoing')
    apply_link = models.URLField(null=True,blank=True)
    apply_last_date=models.DateField(null=True,blank=True)
    number_of_hirings = models.PositiveIntegerField(null=True,blank=True)
    description= models.CharField(null=True)

    def __str__(self):
        return f"{self.recruiter}-{self.designation}({self.date})"
    
    
class Recruitment_Participating_Branches(models.Model):
    scheduled_recruitment=models.ForeignKey(Schedule_Recruitment,on_delete=models.CASCADE, null=False)
    program_semester=models.ManyToManyField(Program_Semester)
    
    
   
class Attendence(models.Model):
    training_participant=models.ForeignKey(TrainingParticipant,on_delete=models.CASCADE)
    date = models.DateField()
    present_students = models.ManyToManyField(Student,related_name='present_attendences')
    absent_student=models.ManyToManyField(Student,related_name='absent_attendences')

    def __str__(self):
        return f"{self.date}-{self.training_participant}"
    
class Recruitment_Participated_Students(models.Model):
    scheduled_recruitment=models.ForeignKey(Schedule_Recruitment,on_delete=models.CASCADE, null=False)
    student = models.ForeignKey(Student,on_delete=models.CASCADE, null=False)
    applied_date=models.DateField(null=True)

    def __str__(self):
        return f"{self.student}:{self.scheduled_recruitment}"
    

class Recruitment_Student_Updations(models.Model):
    selection_choices = (
        ('Aptitude', 'Aptitude'),
        ('Group Discussion', 'Group Discussion'),
        ('Exam', 'Exam'),
        ('HR Interview', 'HR Interview'),
        ('Technical Interview', 'Technical Interview'),
        ('Others', 'Others'), 
    )
    is_selected_choices=(
        ('Qualified','Qualified'),
        ('Disqualified','Disqualified'),
    )
    status_choices =(
        ('ongoing','ongoing'),
        ('completed','completed')
    )
    # add others input colum
    recruitment_participated_student=models.ForeignKey(Recruitment_Participated_Students,on_delete=models.CASCADE, null=False)
    date = models.DateField(null=True)
    type_of_selection=models.CharField(max_length=30, choices=selection_choices, null=False)
    others=models.CharField(max_length=60, null=True,blank=True)
    is_selected=models.CharField(max_length=30, choices=is_selected_choices,null=True)
    status = models.CharField(max_length=30, choices=status_choices, default='ongoing') #if exam is pass set ongoing to complete until final process complete

    def __str__(self):
        return f"{self.recruitment_participated_student},{self.type_of_selection}"
    
    def save(self, *args, **kwargs):
        if self.is_selected == 'Disqualified':
            self.status = 'completed'
        super().save(*args, **kwargs)

class Placed_students(models.Model):
    recruitment_participated_student=models.ForeignKey(Recruitment_Participated_Students,on_delete=models.CASCADE, null=False)
    placed_date=models.DateField()
    offer_latter=models.ImageField(upload_to='student_documents/offer_latters/', null=True,blank=True)
    salary_package = models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return f"{self.recruitment_participated_student.student}:Date{self.placed_date}"
    
class Academic_year(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.start_date.year}-{self.end_date.year}"

class Skills(models.Model):
    skill_name = models.CharField(null=False,unique=True)
    def __str__(self):
        return f"{self.skill_name}"

class Student_skills(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=False)
    skill = models.ForeignKey(Skills,on_delete=models.CASCADE,null=False)
    def __str__(self):
        return f"{self.student}-{self.skill}"
    
class Student_Additional_Documents(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=False)
    document = models.ImageField(upload_to='student_documents/additional/', null=False)
    document_name =models.CharField(null=False)
    def __str__(self):
        return f"{self.student}-{self.document_name}"
    
class Student_Resume(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    resume = models.ImageField(upload_to='student_documents/resume/', null=False)
    def __str__(self):
        return f"{self.student}"
    

class alumni_batch_details(models.Model):
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.start_year} - {self.end_year}"
    
class alumni_details(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    address = models.TextField()
    gender = models.CharField(max_length=15)
    phone = models.CharField(max_length=15, null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    batch = models.ForeignKey(alumni_batch_details, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='alumni/profile_picture/', null=True,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}:{self.program}"
    
class   alumni_job(models.Model):
    job_title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    person = models.ForeignKey(alumni_details, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f"{self.person}{self.job_title} at {self.company}"

class Controls(models.Model):
    register = models.BooleanField(default=False)