from rest_framework import serializers
from school.models.taskModel import TaskModel

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ('id', 'description', 'due_date', 'completed')  
