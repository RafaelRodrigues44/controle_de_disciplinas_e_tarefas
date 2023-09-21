from rest_framework import serializers
from school.models.studentModel import Student

# Serializador da model Estudante
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'email')  
