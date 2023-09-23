# Importa as classes necessárias do Django REST framework e do seu projeto Django.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.taskModel import TaskModel  
from school.serializers.taskSerializer import TaskSerializer  
from school.models.studentModel import Student
from school.exceptions.tasksExceptions import NoTaskFoundException, MissingRequiredFieldsException
from school.exceptions.studentExceptions  import StudentNotFoundException


# Define uma classe 'TaskList' que herda de 'APIView'.
class TaskList(APIView):
    # Método para lidar com solicitações GET para listar todas as tarefas.

     def get(self, request):
        """
        Método GET para listar todos os estudantes 

        Returns:
            Response: Uma resposta JSON contendo os estudantes cadastrados ou uma mensagem de que não há estudantes no banco de dados.
        """
        try:
            # Obtém todos os objetos do modelo 'Student'.
            tasks = TaskModel.objects.all()
            
            # Verifica se a lista de estudantes está vazia.
            if not tasks:
                raise NoTaskFoundException
            
            # Serializa os objetos 'students' em formato JSON.
            serializer = TaskSerializer(tasks, many=True)
            
            # Retorna a resposta com os dados serializados.
            return Response(serializer.data)
        except NoTaskFoundException as e:
            # Capturamos a exceção personalizada e retornamos uma resposta com a mensagem adequada.
            return Response({"detail": str(e)}, status=status.HTTP_200_OK)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # Método para criar tarefas na lista
     def post(self, request):
        try:
            # Obtém o ID do estudante a partir dos dados da solicitação
            student_id = request.data.get('student', None)

            # Lista de campos obrigatórios
            required_fields = ['student', 'description', 'due_date','completed', 'disciplines']

            # Verifica campos que estão faltando
            missing_fields = [field for field in required_fields if field not in request.data]

            if missing_fields:
                raise MissingRequiredFieldsException(missing_fields)

            # Verifica se o ID do estudante é válido
            if student_id is not None:
                try:
                    student = Student.objects.get(pk=student_id)
                except Student.DoesNotExist:
                    raise StudentNotFoundException

                serializer = TaskSerializer(data=request.data)
                if serializer.is_valid():
                    # Define o campo 'student' com o objeto do estudante
                    serializer.validated_data['student'] = student
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response("Invalid request!", status=status.HTTP_400_BAD_REQUEST)

        except MissingRequiredFieldsException as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        except StudentNotFoundException:
            return Response("Estudante não encontrado", status=status.HTTP_404_NOT_FOUND)



# Define uma classe 'TaskDetail' que herda de 'APIView'.
class TaskDetail(APIView):
    # Método auxiliar para obter uma tarefa pelo seu ID.
    def get_object(self, id):
        try:
            # Tenta obter uma tarefa pelo ID fornecido.
            return TaskModel.objects.get(id=id)
        except TaskModel.DoesNotExist:
            # Levanta a exceção personalizada se a tarefa não existir.
            raise NoTaskFoundException

    def get(self, request, id):
        try:
            task = self.get_object(id)
            # Serializa os detalhes da tarefa em formato JSON.
            serializer = TaskSerializer(task)
            # Retorna a resposta com os dados serializados da tarefa.
            return Response(serializer.data)
        except :
            # Captura a exceção personalizada e retorna uma resposta com status 404 (Not Found).
            return Response("Task not found in database", status=status.HTTP_404_NOT_FOUND)


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
            # Retorna uma resposta com status 204 (No Content) e a mensagem de confirmação.
            return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)
        # Retorna uma resposta com status 404 (Not Found) se a tarefa não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)
