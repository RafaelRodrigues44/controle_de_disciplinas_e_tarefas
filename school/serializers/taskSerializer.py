from rest_framework import serializers
from school.models.taskModel import TaskModel
from school.models.disciplineModel import Discipline  

# Serializador da model Tarefa
class TaskSerializer(serializers.ModelSerializer):
    
    disciplines_names = serializers.SerializerMethodField()

    class Meta:
        model = TaskModel
        fields = ('id', 'description', 'due_date', 'disciplines_names')  

    def get_disciplines_names(self, obj):
        # Obtém os objetos de Disciplina com base nos IDs no campo 'disciplines' da tarefa
        disciplines = Discipline.objects.filter(id__in=obj.disciplines.all())
        # Retorna uma lista dos nomes das disciplinas
        return [discipline.name for discipline in disciplines]
