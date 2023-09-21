from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer

class StudentTasksList(APIView):
    def get(self, request, student_id, pk):
        """
        Método GET para listar tarefas de um estudante com base no ID do estudante e no ID da tarefa.

        Args:
            request (HttpRequest): A solicitação HTTP recebida.
            student_id (int): O ID do estudante.
            pk (int): O ID da tarefa.

        Returns:
            Response: Uma resposta JSON contendo as tarefas correspondentes.
        """
        # Filtra as tarefas com base no ID do estudante e no ID da tarefa usando o modelo TaskModel.
        tasks = TaskModel.objects.filter(student=student_id, id=pk)
        
        # Serializa as tarefas encontradas usando o serializador TaskSerializer.
        serializer = TaskSerializer(tasks, many=True)
        
        # Retorna uma resposta HTTP com os dados serializados das tarefas.
        return Response(serializer.data)
