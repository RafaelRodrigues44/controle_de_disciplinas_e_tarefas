# Importa as classes necessárias do Django REST framework e do seu projeto Django.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel  # Importa o modelo de dados 'TaskModel'.
from school.serializers.taskSerializer import TaskSerializer  # Importa o serializador 'TaskSerializer'.

# Define uma classe 'TaskList' que herda de 'APIView'.
class TaskList(APIView):
    # Método para lidar com solicitações GET para listar todas as tarefas.
    def get(self, request):
        tasks = TaskModel.objects.all()
        # Serializa os objetos 'tasks' em formato JSON usando o serializador 'TaskSerializer'.
        serializer = TaskSerializer(tasks, many=True)
        # Retorna a resposta com os dados serializados.
        return Response(serializer.data)

    # Método para lidar com solicitações POST para criar uma nova tarefa.
    def post(self, request):
        # Serializa os dados da solicitação em um novo objeto 'TaskModel'.
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Salva a nova tarefa no banco de dados.
            serializer.save()
            # Retorna os dados serializados da nova tarefa com status 201 (Created).
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Em caso de dados inválidos, retorna uma resposta de erro com status 400.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define uma classe 'TaskDetail' que herda de 'APIView'.
class TaskDetail(APIView):
    # Método auxiliar para obter uma tarefa pelo seu ID.
    def get_object(self, id):
        try:
            # Tenta obter uma tarefa pelo ID fornecido.
            return TaskModel.objects.get(id=id)
        except TaskModel.DoesNotExist:
            # Retorna None se a tarefa não existir.
            return None

    # Método para lidar com solicitações GET para obter detalhes de uma tarefa pelo seu ID.
    def get(self, request, id):
        task = self.get_object(id)
        if task is not None:
            # Serializa os detalhes da tarefa em formato JSON.
            serializer = TaskSerializer(task)
            # Retorna a resposta com os dados serializados da tarefa.
            return Response(serializer.data)
        # Retorna uma resposta com status 404 (Not Found) se a tarefa não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Método para lidar com solicitações PUT para atualizar os detalhes de uma tarefa pelo seu ID.
    def put(self, request, id):
        task = self.get_object(id)
        if task is not None:
            # Serializa os dados da solicitação e atualiza a tarefa.
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Retorna os dados serializados da tarefa atualizada.
                return Response(serializer.data)
            # Em caso de dados inválidos, retorna uma resposta de erro com status 400.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Retorna uma resposta com status 404 (Not Found) se a tarefa não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Método para lidar com solicitações DELETE para excluir uma tarefa pelo seu ID.
    def delete(self, request, id):
        task = self.get_object(id)
        if task is not None:
            # Exclui a tarefa do banco de dados.
            task.delete()
            # Retorna uma resposta com status 204 (No Content) para indicar a exclusão bem-sucedida.
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Retorna uma resposta com status 404 (Not Found) se a tarefa não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)
