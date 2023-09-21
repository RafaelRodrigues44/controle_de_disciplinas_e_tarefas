from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer

class DisciplineTasksList(APIView):
    def get(self, request, discipline_id, pk):
        """
        Método GET para listar tarefas de uma disciplina com base no ID da disciplina e no ID da tarefa.

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            discipline_id (int): O ID da disciplina.
            pk (int): O ID da tarefa.

        Returns:
            Response: Uma resposta JSON contendo as tarefas correspondentes.
        """
        # Filtra as tarefas com base no ID da disciplina e no ID da tarefa usando o modelo TaskModel.
        tasks = TaskModel.objects.filter(disciplinas=discipline_id, id=pk)
        
        # Serializa as tarefas encontradas usando o serializador TaskSerializer.
        serializer = TaskSerializer(tasks, many=True)
        
        # Retorna uma resposta HTTP com os dados serializados das tarefas.
        return Response(serializer.data)
