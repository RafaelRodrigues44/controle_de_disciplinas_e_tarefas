# Importa as classes necessárias do Django REST framework e do seu projeto Django.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.disciplineModel import Discipline  
from school.serializers.disciplineSerializer import DisciplineSerializer  
from school.exceptions.disciplinesExceptions import DisciplineValidationException, DisciplineNotFoundException, NoDisciplinesFoundException



# Define uma classe 'DisciplineList' que herda de 'APIView'.
class DisciplineList(APIView):
    # Método para lidar com solicitações GET para listar todas as disciplinas.
    def get(self, request):
        """
        Método GET para listar todas as disciplinas.

        Returns:
            Response: Uma resposta JSON contendo as disciplinas.
        """
        disciplines = Discipline.objects.all()
        
        if not disciplines.exists():
            # Se a lista de disciplinas estiver vazia, levante a exceção NoDisciplinesFoundException.
            raise NoDisciplinesFoundException
        
        # Serializa os objetos 'disciplines' em formato JSON usando o serializador 'DisciplineSerializer'.
        serializer = DisciplineSerializer(disciplines, many=True)
        # Retorna a resposta com os dados serializados.
        return Response(serializer.data)

    # Método para lidar com solicitações POST para criar uma nova disciplina.
    def post(self, request):
        """
        Método POST para criar uma disciplina

        Returns:
            Response: Uma resposta JSON contendo a disciplina criada ou mensagens de erro de validação.
        """
        try:
            # Serializa os dados da solicitação em um novo objeto 'Discipline'.
            serializer = DisciplineSerializer(data=request.data)
            # Verifica se os dados são válidos.
            if serializer.is_valid():
                # Salva a nova disciplina no banco de dados.
                serializer.save()
                # Retorna os dados serializados da nova disciplina com status 201 (Created).
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # Em caso de dados inválidos, lança a exceção de validação com as mensagens de erro.
            raise DisciplineValidationException

        except DisciplineValidationException as e:
            # Captura a exceção personalizada e retorna as mensagens de erro de validação.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Define uma classe 'DisciplineDetail' que herda de 'APIView'.
class DisciplineDetail(APIView):
    # Método auxiliar para obter uma disciplina pelo seu ID.
    def get_object(self, id):
        try:
            # Tenta obter uma disciplina pelo ID fornecido.
            return Discipline.objects.get(id=id)
        except Discipline.DoesNotExist:
            # Levanta a exceção DisciplineNotFoundException se a disciplina não existir.
            raise DisciplineNotFoundException
    
    def get(self, request, id):
        """
        Método GET para obter uma disciplina pelo seu ID.

        Returns:
            Response: Uma resposta JSON contendo os dados da disciplina.
        """
        discipline = self.get_object(id)
        if discipline is not None:
            # Serializa a disciplina encontrada em formato JSON usando o serializador 'DisciplineSerializer'.
            serializer = DisciplineSerializer(discipline)
            # Retorna a resposta com os dados serializados.
            return Response(serializer.data)
        # Se a disciplina não for encontrada, a exceção será levantada e tratada automaticamente.
        raise DisciplineNotFoundException


    # Método para lidar com solicitações PUT para atualizar os detalhes de uma disciplina pelo seu ID.
    def put(self, request, id):
        """
        Método PUT para alterar uma  disciplina pelo seu id 

        Returns:
            Response: Uma resposta JSON contendo a discplina buscada.
        """
        discipline = self.get_object(id)
        if discipline is not None:
            # Serializa os dados da solicitação e atualiza a disciplina.
            serializer = DisciplineSerializer(discipline, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # Retorna os dados serializados da disciplina atualizada.
                return Response(serializer.data)
            # Em caso de dados inválidos, retorna uma resposta de erro com status 400.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Retorna uma resposta com status 404 (Not Found) se a disciplina não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Método para lidar com solicitações DELETE para excluir uma disciplina pelo seu ID.
    def delete(self, request, id):
        """
        Método DELETE para listar uma  disciplina pelo seu id 

        Returns:
            Response: Uma resposta JSON contendo a discplina deletada.
        """
        discipline = self.get_object(id)
        
        if discipline is not None:
            # Verifica se existem tarefas associadas a esta disciplina.
            related_tasks = discipline.taskmodel_set.all()
            
            if related_tasks.exists():
                # Se houver tarefas associadas, percorra todas e remova a associação com a disciplina.
                for task in related_tasks:
                    task.disciplines.remove(discipline)
            
            # Em seguida, exclua a disciplina.
            discipline.delete()
            return Response("Discipline deleted!", status=status.HTTP_204_NO_CONTENT)
        
        raise DisciplineNotFoundException
