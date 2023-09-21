from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer
from rest_framework.views import APIView

class StudentTasksList(APIView):
    def get(self, request, student_id):
        """
        Método GET para listar todas as tarefas de um estudante com base no ID do estudante.

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            student_id (int): O ID do estudante.

        Returns:
            Response: Uma resposta JSON contendo as tarefas do estudante.
        """
        # Filtra as tarefas com base no ID do estudante usando o modelo TaskModel.
        tasks = TaskModel.objects.filter(student=student_id)
        
        # Serializa as tarefas encontradas usando o serializador TaskSerializer.
        serializer = TaskSerializer(tasks, many=True)
        
        # Retorna uma resposta HTTP com os dados serializados das tarefas do estudante.
        return Response(serializer.data)
