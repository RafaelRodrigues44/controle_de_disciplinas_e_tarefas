# Importa as classes necessárias do Django REST framework e do seu projeto Django.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.disciplineModel import Discipline  # Importa o modelo de dados 'Discipline'.
from school.serializers.disciplineSerializer import DisciplineSerializer  # Importa o serializador 'DisciplineSerializer'.

# Define uma classe 'DisciplineList' que herda de 'APIView'.
class DisciplineList(APIView):
    # Método para lidar com solicitações GET para listar todas as disciplinas.
    def get(self, request):
        disciplines = Discipline.objects.all()
        # Serializa os objetos 'disciplines' em formato JSON usando o serializador 'DisciplineSerializer'.
        serializer = DisciplineSerializer(disciplines, many=True)
        # Retorna a resposta com os dados serializados.
        return Response(serializer.data)

    # Método para lidar com solicitações POST para criar uma nova disciplina.
    def post(self, request):
        # Serializa os dados da solicitação em um novo objeto 'Discipline'.
        serializer = DisciplineSerializer(data=request.data)
        if serializer.is_valid():
            # Salva a nova disciplina no banco de dados.
            serializer.save()
            # Retorna os dados serializados da nova disciplina com status 201 (Created).
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Em caso de dados inválidos, retorna uma resposta de erro com status 400.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Define uma classe 'DisciplineDetail' que herda de 'APIView'.
class DisciplineDetail(APIView):
    # Método auxiliar para obter uma disciplina pelo seu ID.
    def get_object(self, id):
        try:
            # Tenta obter uma disciplina pelo ID fornecido.
            return Discipline.objects.get(id=id)
        except Discipline.DoesNotExist:
            # Retorna None se a disciplina não existir.
            return None

    # Método para lidar com solicitações GET para obter detalhes de uma disciplina pelo seu ID.
    def get(self, request, id):
        discipline = self.get_object(id)
        if discipline is not None:
            # Serializa os detalhes da disciplina em formato JSON.
            serializer = DisciplineSerializer(discipline)
            # Retorna a resposta com os dados serializados da disciplina.
            return Response(serializer.data)
        # Retorna uma resposta com status 404 (Not Found) se a disciplina não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Método para lidar com solicitações PUT para atualizar os detalhes de uma disciplina pelo seu ID.
    def put(self, request, id):
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
        discipline = self.get_object(id)
        if discipline is not None:
            # Certifique-se de desassociar as tarefas relacionadas a esta disciplina
            discipline.tasks.clear()
            # Exclui a disciplina do banco de dados.
            discipline.delete()
            # Retorna uma resposta com status 204 (No Content) para indicar a exclusão bem-sucedida.
            return Response(status=status.HTTP_204_NO_CONTENT)
        # Retorna uma resposta com status 404 (Not Found) se a disciplina não existir.
        return Response(status=status.HTTP_404_NOT_FOUND)
