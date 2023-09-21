from django.urls import path
from school.views.studentView import StudentDetail, StudentList
from school.views.disciplineView import  DisciplineList, DisciplineDetail
from school.views.taskView import TaskDetail, TaskList
from school.views.disciplineTaskView import DisciplineTasksList
from school.views.studentTaskView import StudentTasksList

schoolUrls = [
    path('students/', StudentList.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('disciplines/', DisciplineList.as_view(), name='disciplines-list'),
    path('disciplines/<int:id>/', DisciplineDetail.as_view(), name='disciplines-detail'),
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/<int:id>/', TaskDetail.as_view(), name='task-detail'),
    path('students/<int:student_id>/tasks/', StudentTasksList.as_view(), name='student-tasks-list'),
    path('disciplines/<int:discipline_id>/tasks/', DisciplineTasksList.as_view(), name='discipline-tasks-list'),
]