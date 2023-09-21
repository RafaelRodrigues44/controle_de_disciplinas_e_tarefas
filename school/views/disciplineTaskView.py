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
        try:
            # Filtra as tarefas com base no ID da disciplina.
            tasks = TaskModel.objects.filter(disciplines=discipline_id, id=pk)
            
            # Verifica se a tarefa com o ID especificado pertence à disciplina.
            task = tasks.first()
            if task:
                # Serializa a tarefa encontrada usando o serializador TaskSerializer.
                serializer = TaskSerializer(task)
                return Response(serializer.data)
            else:
                return Response({'error': 'Tarefa não encontrada nesta disciplina.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
