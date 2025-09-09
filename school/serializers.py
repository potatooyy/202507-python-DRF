# school/serialiers.py

from rest_framework import serializers
from .models import Teacher, Student

class TeacherSimpleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teacher
        fields = ['id', 'teacher_name', 'title', 'department_id']

class StudentSimpleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'student_name', 'class_id']

class TeacherSerializer(serializers.ModelSerializer):
    mentees = StudentSimpleSerializer(many=True, read_only=True)
    advisees = StudentSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = [
                    'id', 
                    'teacher_name', 
                    'staff_id', 
                    'title', 
                    'department_id', 
                    'created_at', 
                    'mentees',
                    'advisees'
                ]

class StudentSerializer(serializers.ModelSerializer):
    mentor = TeacherSimpleSerializer(read_only=True)
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        write_only=True,
        source='mentor',
        required=False,
        allow_null=True 
    )
    advisor = TeacherSimpleSerializer(read_only=True)
    advisor_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(),
        write_only=True,
        source='advisor',
        required=False,
        allow_null=True 
    )
    class Meta:
        model = Student
        fields = [
                    'id',
                    'student_name', 
                    'student_id', 
                    'role', 
                    'department_id', 
                    'enroll_year',
                    'grade',
                    'class_id',
                    'mentor',
                    'mentor_id', 
                    'advisor',
                    'advisor_id',
                    'created_at'
                  ]