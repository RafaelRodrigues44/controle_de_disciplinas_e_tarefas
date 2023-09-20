from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from school.models.disciplineModel import Discipline
from school.serializers.disciplineSerializer import DisciplineSerializer

class DisciplineList(APIView):
    def get(self, request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DisciplineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DisciplineDetail(APIView):
    def get_object(self, id):
        try:
            return Discipline.objects.get(id=id)
        except Discipline.DoesNotExist:
            return None

    def get(self, request, id):
        discipline = self.get_object(id)
        if discipline is not None:
            serializer = DisciplineSerializer(discipline)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        discipline = self.get_object(id)
        if discipline is not None:
            serializer = DisciplineSerializer(discipline, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        discipline = self.get_object(id)
        if discipline is not None:
            # Certifique-se de desassociar as tarefas relacionadas a esta disciplina
            discipline.tasks.clear()
            discipline.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
