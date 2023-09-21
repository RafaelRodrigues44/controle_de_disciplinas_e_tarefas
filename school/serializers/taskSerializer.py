from rest_framework import serializers
from school.models.taskModel import TaskModel

# Serializador da model Tarefa
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ('id', 'description', 'due_date', 'completed')  
