from django.urls import path
from school.views.studentView import StudentDetail, StudentList
from school.views.disciplineView import  DisciplineList, DisciplineDetail
from school.views.taskView import TaskDetail, TaskList
from school.views.disciplineTaskView import DisciplineTasksList
from school.views.studentTaskView import StudentTasksList

urlpatterns = [
    path('api/alunos/', StudentList.as_view(), name='student-list'),
    path('api/alunos/<int:id>/', StudentDetail.as_view(), name='student-detail'),
    path('api/disciplines/', DisciplineList.as_view(), name='disciplines-list'),
    path('api/disciplines/<int:id>/', DisciplineDetail.as_view(), name='disciplines-detail'),
    path('api/tasks/', TaskList.as_view(), name='task-list'),
    path('api/tasks/<int:id>/', TaskDetail.as_view(), name='task-detail'),
    path('api/students/<int:student_id>/tasks/', StudentTasksList.as_view(), name='student-tasks-list'),
    path('api/disciplines/<int:discipline_id>/tasks/', DisciplineTasksList.as_view(), name='discipline-tasks-list'),
]