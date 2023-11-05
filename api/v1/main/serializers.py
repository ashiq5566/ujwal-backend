# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from accounts.models import User
from main.models import *


class DepartmentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        exclude = ['department_id']
        
    def update(self, instance, validated_data):
        instance.department_name = validated_data.get('department_name', instance.department_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        
        return instance

class DepartmentsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'

class TrainerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainers
        exclude = ['trainer_id']
        
    def update(self, instance, validated_data):
        instance.trainer_name = validated_data.get('trainer_name', instance.trainer_name)
        instance.training_company = validated_data.get('training_company', instance.training_company)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.website = validated_data.get('website', instance.website)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        
        return instance

class TrainersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainers
        fields = '__all__'

class RecruiterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiters
        exclude = ['recruiter_id']
        
    def update(self, instance, validated_data):
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)
        instance.website = validated_data.get('website', instance.website)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        
        return instance
        
        

class RecruitersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiters
        fields = '__all__'

class ProgramPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        exclude = ['program_id']
        
    def update(self, instance, validated_data):
        instance.program_name = validated_data.get('program_name', instance.program_name)
        department = validated_data.get('department', instance.department)
        department_pk = department.pk
        if Departments.objects.filter(pk=department_pk).exists():
            department = Departments.objects.get(pk=department_pk)
            instance.department = department
        instance.type = validated_data.get('type', instance.type)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.number_of_semester = validated_data.get('number_of_semester', instance.number_of_semester)
        instance.save()
        
        return instance

class ProgramsGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programs
        fields = '__all__'
        
class ProgramsGetWithDepartmentSerializer(serializers.ModelSerializer):
    department_details = serializers.SerializerMethodField()
    class Meta:
        model = Programs
        fields = '__all__'

    def get_department_details(self, obj):
        dep_id = obj.department.id
        filtered_data = Departments.objects.get(pk=dep_id)
        serialized_data = DepartmentsGetSerializer(filtered_data, many=False).data
        return serialized_data
        

class FocusinAreaGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusingArea
        fields = '__all__'


class SemestersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semesters
        fields = '__all__'

class ProgramSemesterGetSerializer(serializers.ModelSerializer):
    program_name =serializers.SerializerMethodField()
    semester_name =serializers.SerializerMethodField()
    class Meta:
        model = Program_Semester
        fields = '__all__'
    def get_program_name(self, obj):
        return obj.program.program_name
    def get_semester_name(self, obj):
        return obj.semester.semester

class TrainingScheduleSerializer(serializers.Serializer):
    trainer_id = serializers.IntegerField()
    start_date_str = serializers.CharField()
    created_date_str = serializers.CharField()
    end_date_str = serializers.CharField()
    venue = serializers.CharField()
    foc_areas_ids = serializers.ListField(child=serializers.IntegerField())
    participants_ids = serializers.ListField(child=serializers.IntegerField())
    

class EditTrainingScheduleSerializer(serializers.Serializer):
    trainer_id = serializers.IntegerField()
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    venue = serializers.CharField()
    focusing_area = serializers.ListField(child=serializers.IntegerField())
    participants_ids = serializers.ListField(child=serializers.IntegerField())
    
    def update(self, instance, validated_data):
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.venue = validated_data.get('venue', instance.venue)
        focusing_area_data = validated_data.get('focusing_area', instance.focusing_area.all())
        instance.focusing_area.set(focusing_area_data)
        instance.save()
        
        participants_ids = validated_data.get('participants_ids')

        if Program_Semester.objects.filter(id__in=participants_ids).exists():

            training_participants = TrainingParticipant.objects.filter(allot_trainer__pk=instance.pk)
            participants = Program_Semester.objects.filter(id__in=participants_ids)
            participants_iterator = iter(participants)
            
            # existing program semester ids
            program_sem_ids = TrainingParticipant.objects.filter(allot_trainer__pk=instance.pk).values_list('program_semester') 
            
            for training_participant in training_participants:
                try:
                    participant = next(participants_iterator)
                except StopIteration:
                    break
                if not participant in program_sem_ids:
                    training_participant.program_semester = participant
                    training_participant.save()
        
        return instance
    

class TrainingSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllotTrainer
        fields = '__all__'
    

class RecruitmentScheduleSerializer(serializers.Serializer):
    recruiter_id = serializers.IntegerField()
    date = serializers.CharField()  
    venue = serializers.CharField()
    designation = serializers.CharField()
    participants_ids = serializers.ListField(child=serializers.IntegerField())
    apply_link = serializers.URLField()
    number_of_hirings = serializers.IntegerField()
    apply_last_date = serializers.CharField() 
    description =  serializers.CharField() 
    

class RecruitmentSchedulesSerializer(serializers.ModelSerializer):
    participents_details = serializers.SerializerMethodField()
    recruiter_name =serializers.CharField(source='recruiter.company_name')

    class Meta:
        model = Schedule_Recruitment
        fields = '__all__'

    def get_participents_details(self, obj):
        schedule_id = obj.id
        filtered_data = Recruitment_Participating_Branches.objects.filter(scheduled_recruitment_id=schedule_id)
        serialized_data = RecruitmentParticipentsSerializer(filtered_data, many=True).data
        return serialized_data

class TrainingParticipentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingParticipant
        fields = '__all__'

class RecruitmentParticipentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Participating_Branches
        fields = '__all__'

class RecruitmentParticipentsSerializer(serializers.ModelSerializer):
    program_semester = serializers.SerializerMethodField()
    class Meta:
        model = Recruitment_Participating_Branches
        fields = ['scheduled_recruitment','program_semester']

    def get_program_semester(self, obj):
        program_semesters = obj.program_semester.all()  # Assuming you want to retrieve all related Program_Semester instances
        serialized_program_semesters = []  # List to store serialized Program_Semester data
        for program_semester in program_semesters:
            serialized_program_semester = {
                'program_semester': program_semester.id,  # You can customize the fields you want to include
                'department': program_semester.program.department.id,  # You can customize the fields you want to include
                'program': program_semester.program.id,  # You can customize the fields you want to include
                'program_name': program_semester.program.program_name,  # You can customize the fields you want to include
                'semester': program_semester.semester.id,
                'semester_name': program_semester.semester.semester,
            }
            serialized_program_semesters.append(serialized_program_semester)
        return serialized_program_semesters       
        
class AttendancePostSerializer(serializers.Serializer):
    date = serializers.CharField()
    absent_student = serializers.ListField(child=serializers.IntegerField())
    present_student = serializers.ListField(child=serializers.IntegerField())
    

class StudentProgramSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_program_semester
        fields = '__all__'
        
class RecruitmentParticipatedStudentsSchedulesSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='student.program.program_name')
    program_name = serializers.CharField(source='student.program.department.department_name')
    admission_number = serializers.CharField(source='student.admission_number')
    first_name = serializers.CharField(source='student.first_name')
    last_name = serializers.CharField(source='student.last_name')
    gender = serializers.CharField(source='student.gender')
    roll_number = serializers.CharField(source='student.roll_number')
    designation = serializers.CharField(source='scheduled_recruitment.designation')
    semester_marks = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    class Meta:
        model = Recruitment_Participated_Students
        fields = '__all__'

    def get_semester_marks(self, instance):
        marks = Student_program_semester.objects.filter(student=instance.student).order_by('semester__semester__semester')
        seralizer = searchMarklisteSerialiser(marks,many=True)
        return seralizer.data
    def get_resume(self, instance):
        if Student_Resume.objects.filter(student=instance.student).exists():
            reusme = Student_Resume.objects.filter(student=instance.student)
            seralizer = StudentResumeSerializer(reusme,many=True)
            return seralizer.data
        return None
    
class PostRecruitmentParticipatedStudentsSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Participated_Students
        fields = '__all__'
class RecruitmentSelectionUpdatesSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruitment_Student_Updations
        fields = '__all__'

class ParticipatedStudentsByRecruitmentSchedulesSerializer(serializers.ModelSerializer):
    participated_id = serializers.IntegerField(source='id')
    class Meta:
        model = Recruitment_Participated_Students
        fields = ['participated_id','student']

class PlacedPOSTStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placed_students
        fields = '__all__'

class PlacedStudentsSerializer(serializers.ModelSerializer):
    admission_number = serializers.CharField(source='recruitment_participated_student.student.admission_number')
    first_name = serializers.CharField(source='recruitment_participated_student.student.first_name')
    last_name = serializers.CharField(source='recruitment_participated_student.student.last_name')
    gender = serializers.CharField(source='recruitment_participated_student.student.gender')
    roll_number = serializers.CharField(source='recruitment_participated_student.student.roll_number')
    recruiter_company_name = serializers.CharField(source='recruitment_participated_student.scheduled_recruitment.recruiter.company_name')
    recruiter_designation = serializers.CharField(source='recruitment_participated_student.scheduled_recruitment.designation')
    program_name = serializers.CharField(source='recruitment_participated_student.student.program.program_name')
    department_name = serializers.CharField(source='recruitment_participated_student.student.program.department.department_name')
    
    class Meta:
        model = Placed_students
        fields = ['admission_number', 'first_name', 'last_name', 'gender','roll_number',
                  'recruiter_company_name', 'recruiter_designation', 'program_name', 'department_name', 'placed_date','offer_latter','salary_package']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendence
        fields = '__all__'

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_year
        fields = '__all__'

class StudentAdditionalDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Additional_Documents
        fields = '__all__'

class StudentResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student_Resume
        fields = '__all__'
        
class StudentReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
class StudentAcademicDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAcademicDetails
        fields = '__all__'

class ControlGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Controls
        fields = '__all__'
class AlumniDetailsSerializer(serializers.ModelSerializer):
    batch_start = serializers.SerializerMethodField()
    batch_end = serializers.SerializerMethodField()
    jobDetails = serializers.SerializerMethodField()
    program_name = serializers.SerializerMethodField()

    class Meta:
        model = alumni_details
        fields = '__all__'
    

    def get_program_name(self, instance):
        return instance.program.program_name
    
    def get_batch_start(self, instance):
        return instance.batch.start_year

    def get_batch_end(self, instance):
        return instance.batch.end_year

    def get_jobDetails(self, instance):
        job_details = alumni_job.objects.filter(person=instance)
        job_details_serializer = AlumniJobSeraliser(job_details, many=True)
        return job_details_serializer.data


class AlumniJobSeraliser(serializers.ModelSerializer):
     class Meta:
        model = alumni_job
        fields = '__all__'


class AlumniRegisterSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    gender = serializers.CharField()
    dateOfBirth = serializers.DateField()
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    program = serializers.IntegerField()
    startYear = serializers.IntegerField()
    endYear = serializers.IntegerField()

class TrainingParticipantForStudentDetailsSerializer(serializers.Serializer):
    training_id = serializers.IntegerField()
    trainer_name = serializers.CharField()
    venue = serializers.CharField()
    status = serializers.CharField()
    focus_areas = serializers.ListField(child=serializers.CharField())
    start_date =serializers.DateField()
    end_date =serializers.DateField()

class TrainingReviewForStudentDetailsSerializer(serializers.Serializer):
    training_id = serializers.IntegerField()
    trainer_name = serializers.CharField()
    venue = serializers.CharField()
    status = serializers.CharField()
    focus_areas = serializers.ListField(child=serializers.CharField())
    start_date =serializers.DateField()
    end_date =serializers.DateField()
    review_marked =serializers.BooleanField()


class TrainingFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_Feedback
        fields = '__all__'

class StudentMarklistSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    start_date = serializers.DateField(allow_null=True, format="%Y-%m-%d")
    end_date = serializers.DateField(allow_null=True, format="%Y-%m-%d")
    sem_status = serializers.CharField()
    marklist_appove_status = serializers.CharField()
    marklist = serializers.CharField(allow_blank=True)
    backlog_count = serializers.IntegerField()
    cgpa = serializers.FloatField()
    semester = serializers.CharField()

# class StudentProgramMarklistSemesterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student_program_semester
#         fields = ('start_date', 'end_date', 'semester')

#     def to_representation(self, instance):
#         return {
#             'start_date': instance['start_date'],
#             'end_date': instance['end_date'],
#             'semester': instance['semester'],
#         }

# class StudentProgramMarklistSemesterSerializer(serializers.ModelSerializer):
#     semester = serializers.SerializerMethodField()
#     semester_name = serializers.SerializerMethodField()
#     program_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Student_program_semester
#         fields = ('start_date', 'end_date', 'semester_name', 'program_name', 'semester')

#     def get_semester(self, instance):
#         return instance['semester'],

#     def get_semester_name(self, instance):
#         return instance['semester__semester__semester'],


#     def get_program_name(self, instance):
#         return instance['semester__program__program_name']

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['id'] = self.get_semester(instance)
#         representation['semester_name'] = self.get_semester_name(instance)
#         representation['program_name'] = self.get_program_name(instance)
        # return representation
    
class DistinctCombinationsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    semester_name = serializers.CharField(source='semester__semester__semester')
    program_name = serializers.CharField(source='semester__program__program_name')
    program_semester_id = serializers.IntegerField(source='semester')

    class Meta:
        fields = ('start_date', 'end_date', 'semester_name', 'program_name', 'semester_id')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['admission_number','first_name','last_name','date_of_birth','gender','roll_number']

class StudentProgramSemesterMarklistSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)

    class Meta:
        model = Student_program_semester
        fields = '__all__'

class searchResumeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Student_Resume
        fields = ['resume']

class searchMarklisteSerialiser(serializers.ModelSerializer):
    semester_name = serializers.SerializerMethodField()
    class Meta:
        model = Student_program_semester
        fields = ['marklist_appove_status','marklist','backlog_count','cgpa','semester_name']
    def get_semester_name(self, instance):
        return instance.semester.semester.semester
class searchAdditionalDocumentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Student_Additional_Documents
        fields = ['document','document_name']

class MarklistDetailsStudentSeralizer(serializers.ModelSerializer):
    semester_name = serializers.SerializerMethodField()
    class Meta:
        model = Student_program_semester
        fields = '__all__'
    def get_semester_name(self, instance):
        return instance.semester.semester.semester