
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models import Student 
from school.serializers.studentSerializer import StudentSerializer 
from school.exceptions.studentExceptions import NoStudentsFoundException
from school.exceptions.studentExceptions import EmptyFieldsException, StudentNotFoundException
from rest_framework.exceptions import ValidationError


# Define uma classe 'StudentList' que herda de 'APIView'.
class StudentList(APIView):
    # Método para lidar com solicitações GET para listar todos os estudantes.
    def get(self, request):
        """
        Método GET para listar todos os estudantes 

        Returns:
            Response: Uma resposta JSON contendo os estudantes cadastrados ou uma mensagem de que não há estudantes no banco de dados.
        """
        try:
            # Obtém todos os objetos do modelo 'Student'.
            students = Student.objects.all()
            
            # Verifica se a lista de estudantes está vazia.
            if not students:
                raise NoStudentsFoundException
            
            # Serializa os objetos 'students' em formato JSON.
            serializer = StudentSerializer(students, many=True)
            
            # Retorna a resposta com os dados serializados.
            return Response(serializer.data)
        except NoStudentsFoundException as e:
            # Capturamos a exceção personalizada e retornamos uma resposta com a mensagem adequada.
            return Response({"detail": str(e)}, status=status.HTTP_200_OK)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # Método para lidar com solicitações POST para criar um novo estudante.
    def post(self, request):
            """
            Método POST para criar um estudante

            Returns:
                Response: Uma resposta JSON contendo o estudante criado ou mensagens de erro de validação.
            """
            try:
                # Verifica se não há dados na solicitação POST.
                if not request.data:
                    raise EmptyFieldsException(["field1", "field2"])  

                # Serializa os dados da solicitação em um novo objeto 'Student'.
                serializer = StudentSerializer(data=request.data)
                # Verifica se os dados são válidos.
                if serializer.is_valid():
                    # Salva o novo estudante no banco de dados.
                    serializer.save()
                    # Retorna os dados serializados do novo estudante com status 201 (Created).
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                # Em caso de dados inválidos, lança uma exceção de validação com as mensagens de erro.
                raise ValidationError(serializer.errors)

            except EmptyFieldsException as e:
                # Captura a exceção personalizada para campos vazios e retorna a mensagem adequada.
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except ValidationError as e:
                # Captura a exceção de validação e retorna as mensagens de erro de validação.
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Em caso de erro, retorna uma resposta de erro com status 500.
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Define uma classe 'StudentDetail' que herda de 'APIView'.
class StudentDetail(APIView):
     # Método auxiliar para obter um objeto 'Student' pelo seu ID (pk).
    def get_object(self, pk):
        try:
            # Tenta obter um estudante pelo ID (pk) fornecido.
            student = Student.objects.get(pk=pk)
            return student
        except Student.DoesNotExist:
            # Lança a exceção personalizada quando o estudante não é encontrado.
            raise StudentNotFoundException
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # Método para lidar com solicitações GET para obter detalhes de um estudante pelo seu ID.
    def get(self, request, pk):
        """
        Método GET para listar uma  estudante pelo seu id 

        Returns:
            Response: Uma resposta JSON contendo o estudante buscada.
        """
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
        """
        Método PUT para alterar dados de um aluno pelo seu id 

        Returns:
            Response: Uma resposta JSON contendo todos os campos do cadastro do aluno, inclusive o alterado.
        """
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
        """
        Método DELETE para apagar dados de um aluno pelo seu id 

        Returns:
            Response: Uma resposta informando que a exclusão foi um sucesso ou no caso de fracasso uma exceção.
        """
        try:
            # Obtém o objeto 'Student' pelo ID (pk).
            student = self.get_object(pk)
            if student is not None:
                # Exclui o estudante do banco de dados.
                student.delete()
                # Retorna uma resposta com status 204 (No Content) para indicar a exclusão bem-sucedida.
                return Response({"message": "Student success deleted"}, status=status.HTTP_204_NO_CONTENT)
            # Retorna uma resposta com status 404 (Not Found) se o estudante não existir.
            return Response(status=status.HTTP_404_NOT_FOUND)
        except StudentNotFoundException as e:
            # Captura a exceção personalizada quando o estudante não é encontrado.
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Em caso de erro, retorna uma resposta de erro com status 500.
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

