# Importa as classes necessárias do Django REST framework e do seu projeto Django.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models import Student  # Importa o modelo de dados 'Student'.
from school.serializers.studentSerializer import StudentSerializer  # Importa o serializador 'StudentSerializer'.

# Define uma classe 'StudentList' que herda de 'APIView'.
class StudentList(APIView):
    # Método para lidar com solicitações GET para listar todos os estudantes.
    def get(self, request):
        try:
            # Obtém todos os objetos do modelo 'Student'.
            students = Student.objects.all()
            # Serializa os objetos 'students' em formato JSON.
            serializer = StudentSerializer(students, many=True)
            # Retorna a resposta com os dados serializados.
            return Response(serializer.data)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Método para lidar com solicitações POST para criar um novo estudante.
    def post(self, request):
        try:
            # Verifica se não há dados na solicitação POST.
            if not request.data:
                return Response(
                    {"error": "JSON vazio. Preencha os campos obrigatórios."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Serializa os dados da solicitação em um novo objeto 'Student'.
            serializer = StudentSerializer(data=request.data)
            # Verifica se os dados são válidos.
            if serializer.is_valid():
                # Salva o novo estudante no banco de dados.
                serializer.save()
                # Retorna os dados serializados do novo estudante com status 201 (Created).
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Em caso de dados inválidos, retorna uma resposta de erro com status 400.
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Define uma classe 'StudentDetail' que herda de 'APIView'.
class StudentDetail(APIView):
    # Método auxiliar para obter um objeto 'Student' pelo seu ID (pk).
    def get_object(self, pk):
        try:
            # Tenta obter um estudante pelo ID (pk) fornecido.
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            # Retorna None se o estudante não existir.
            return None
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Método para lidar com solicitações GET para obter detalhes de um estudante pelo seu ID.
    def get(self, request, pk):
        try:
            # Obtém o objeto 'Student' pelo ID (pk).
            student = self.get_object(pk)
            if student is not None:
                # Serializa os detalhes do estudante em formato JSON.
                serializer = StudentSerializer(student)
                # Retorna a resposta com os dados serializados do estudante.
                return Response(serializer.data)
            # Retorna uma resposta com status 404 (Not Found) se o estudante não existir.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Método para lidar com solicitações PUT para atualizar os detalhes de um estudante pelo seu ID.
    def put(self, request, pk):
        try:
            # Obtém o objeto 'Student' pelo ID (pk).
            student = self.get_object(pk)
            if student is not None:
                # Serializa os dados da solicitação e atualiza o estudante.
                serializer = StudentSerializer(student, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    # Retorna os dados serializados do estudante atualizado.
                    return Response(serializer.data)
                # Em caso de dados inválidos, retorna uma resposta de erro com status 400.
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # Retorna uma resposta com status 404 (Not Found) se o estudante não existir.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Método para lidar com solicitações DELETE para excluir um estudante pelo seu ID.
    def delete(self, request, pk):
        try:
            # Obtém o objeto 'Student' pelo ID (pk).
            student = self.get_object(pk)
            if student is not None:
                # Exclui o estudante do banco de dados.
                student.delete()
                # Retorna uma resposta com status 204 (No Content) para indicar a exclusão bem-sucedida.
                return Response(status=status.HTTP_204_NO_CONTENT)
            # Retorna uma resposta com status 404 (Not Found) se o estudante não existir.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
