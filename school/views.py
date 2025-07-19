# school/views.py
# from django.shortcuts import render
from rest_framework import viewsets
from .models import Teacher, Student
from .serializers import TeacherSerializer, TeacherSimpleSerializer, StudentSerializer, StudentSimpleSerializer
# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer