from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer

class DisciplineTasksList(APIView):
    def get(self, request, discipline_id):
        """
        Método GET para listar todas as tarefas de uma disciplina com base no ID da disciplina.

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            discipline_id (int): O ID da disciplina.

        Returns:
            Response: Uma resposta JSON contendo as tarefas da disciplina.
        """
        try:
            # Filtra as tarefas com base no ID da disciplina.
            tasks = TaskModel.objects.filter(disciplines=discipline_id)
            
            # Serializa as tarefas encontradas usando o serializador TaskSerializer.
            serializer = TaskSerializer(tasks, many=True)
            
            # Retorna uma resposta HTTP com os dados serializados das tarefas da disciplina.
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
