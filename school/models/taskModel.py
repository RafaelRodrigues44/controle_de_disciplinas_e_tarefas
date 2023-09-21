# Importe as classes necessárias do Django
from django.db import models
from school.models.studentModel import Student
from school.models.disciplineModel import Discipline

# Defina o modelo TaskModel, que representa uma tarefa
class TaskModel(models.Model):
    # Crie um campo ForeignKey para relacionar a tarefa com um estudante
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    
    # Relacionamento many to many com  disciplines
    disciplines = models.ManyToManyField(Discipline)

    def __str__(self):
        return self.description
