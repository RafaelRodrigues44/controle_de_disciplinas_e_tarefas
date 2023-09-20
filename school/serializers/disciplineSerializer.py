from rest_framework import serializers
from school.models.disciplineModel import Discipline

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ('id', 'name', 'description')  
