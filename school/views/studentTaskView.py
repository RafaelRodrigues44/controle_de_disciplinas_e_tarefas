from rest_framework.response import Response
from rest_framework import status
from school.models.studentModel import Student
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer
from rest_framework.views import APIView
from school.exceptions.studentTasksExceptions import StudentNotFoundException, NoTasksFoundException

class StudentTasksList(APIView):
    def get(self, request, student_id):
        try:
            # Tente buscar o aluno com base no ID.
            student = Student.objects.get(id=student_id)
            
            # Verifique se o aluno foi encontrado na base de dados.
            if not student:
                # Se o aluno não foi encontrado, lance a exceção personalizada.
                raise StudentNotFoundException
            
            # Tente buscar as tarefas associadas ao aluno usando o modelo TaskModel.
            tasks = TaskModel.objects.filter(student=student)
            
            # Verifique se o aluno tem atividades associadas.
            if not tasks:
                # Se não foram encontradas tarefas, lance a exceção personalizada.
                raise NoTasksFoundException
            
            # Serializa as tarefas encontradas usando o serializador TaskSerializer.
            serializer = TaskSerializer(tasks, many=True)
            
            # Se o aluno foi encontrado e tem atividades, retorne uma resposta HTTP com os dados serializados das tarefas do estudante.
            return Response(serializer.data)
        except StudentNotFoundException as e:
            # Capturamos a exceção personalizada e retornamos um erro HTTP 404 com a mensagem traduzida.
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except NoTasksFoundException as e:
            # Capturamos a exceção personalizada e retornamos um erro HTTP 200 com a mensagem traduzida.
            return Response({"detail": str(e)}, status=status.HTTP_200_OK)
        except Exception as e:
            # Se ocorrer outra exceção, retorne um erro HTTP 500 com a mensagem de erro original.
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
