from django.db import models
from datetime import datetime
# Create your models here.
class Title(models.TextChoices):
    PROFESSOR = 'professor', 'Professor'
    ASSOCIATE_PROFESSOR = 'associate_professor', 'Associate Professor'
    ASSISTANT_PROFESSOR = 'assistant_professor', 'Assistant Professor'
    LECTURER = 'lecturer', 'Lecturer'
class Teacher(models.Model):
    teacher_name = models.CharField(max_length = 64)
    staff_id = models.CharField(max_length= 24, unique=True)
    title = models.CharField(max_length=64, choices=Title.choices, default=Title.LECTURER)
    department_id = models.CharField(max_length = 64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff_id} {self.teacher_name} {self.title}"
    
    class Meta:
        db_table = 'teacher_list'

class Role(models.TextChoices):
    STUDENT = 'student', 'Student'
    CLASS_PRESIDENT = 'class_president', 'Class President'
    CLASS_OFFICER = 'class_officer', 'Class Officer'
class Student(models.Model):
    student_name = models.CharField(max_length = 64)
    student_id = models.CharField(max_length= 24, null = False, unique=True)
    role = models.CharField(max_length=64, choices=Role.choices, default=Role.STUDENT)
    department_id = models.CharField(max_length = 64)
    enroll_year = models.IntegerField()
    class_id = models.CharField(max_length = 16)
    mentor = models.ForeignKey(Teacher, related_name='mentees', on_delete=models.SET_NULL, null=True)
    advisor = models.ForeignKey(Teacher, related_name='advisees', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def grade(self):
        """
        根據 enroll_year 動態計算目前年級
        假設入學後第一年為一年級，八月後進入新學年
        """
        today = datetime.now()
        if today.month >= 8:
            school_year = today.year
        else:
            school_year = today.year - 1
        g = school_year - self.enroll_year +1
        return g if g > 0 else 1

    def __str__(self):
        return f"{self.student_id} {self.student_name}"
    
    class Meta:
        db_table = 'student_list'