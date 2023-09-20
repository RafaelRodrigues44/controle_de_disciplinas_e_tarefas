from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskModelSerializer

class TaskList(APIView):
    def get(self, request):
        tasks = TaskModel.objects.all()
        serializer = TaskModelSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    def get_object(self, id):
        try:
            return TaskModel.objects.get(id=id)
        except TaskModel.DoesNotExist:
            return None

    def get(self, request, id):
        task = self.get_object(id)
        if task is not None:
            serializer = TaskModelSerializer(task)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        task = self.get_object(id)
        if task is not None:
            serializer = TaskModelSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        task = self.get_object(id)
        if task is not None:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
