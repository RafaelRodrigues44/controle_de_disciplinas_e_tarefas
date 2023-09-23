from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.disciplineModel import Discipline
from school.models.taskModel import TaskModel
from school.serializers.taskSerializer import TaskSerializer
from school.exceptions.disciplineTasksExceptions import DisciplineNotFoundException, NoTasksFoundException

class DisciplineTasksList(APIView):
    def get(self, request, discipline_id):
        try:
            # Tente buscar a disciplina com base no ID.
            discipline = Discipline.objects.get(id=discipline_id)
            
            # Verifique se a disciplina foi encontrada na base de dados.
            if not discipline:
                # Se a disciplina não foi encontrada, lance a exceção personalizada.
                raise DisciplineNotFoundException
            
            # Tente buscar as tarefas associadas à disciplina usando o modelo TaskModel.
            tasks = TaskModel.objects.filter(disciplines=discipline)
            
            # Verifique se há tarefas associadas à disciplina.
            if not tasks:
                # Se não foram encontradas tarefas, lance a exceção personalizada.
                raise NoTasksFoundException
            
            # Serializa as tarefas encontradas usando o serializador TaskSerializer.
            serializer = TaskSerializer(tasks, many=True)
            
            # Se a disciplina foi encontrada e tem tarefas, retorne uma resposta HTTP com os dados serializados das tarefas.
            return Response(serializer.data)
        except DisciplineNotFoundException as e:
            # Capturamos a exceção personalizada e retornamos um erro HTTP 404 com a mensagem traduzida.
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except NoTasksFoundException as e:
            # Capturamos a exceção personalizada e retornamos um erro HTTP 200 com a mensagem traduzida.
            return Response({"detail": str(e)}, status=status.HTTP_200_OK)
        except Exception as e:
            # Se ocorrer outra exceção, retorne um erro HTTP 500 com a mensagem de erro original.
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
