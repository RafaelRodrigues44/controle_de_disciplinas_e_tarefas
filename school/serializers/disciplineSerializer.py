from rest_framework import serializers
from school.models.disciplineModel import Discipline

# Serializador da model Disciplina 
class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('id', 'name', 'description')  
