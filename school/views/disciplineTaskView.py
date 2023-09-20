from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer


class DisciplineTasksList(APIView):
    def get(self, request, discipline_id):
        tasks = TaskModel.objects.filter(disciplinas=discipline_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)