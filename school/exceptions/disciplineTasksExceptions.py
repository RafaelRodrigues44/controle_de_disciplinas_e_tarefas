from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class DisciplineNotFoundException(APIException):
    status_code = 404
    default_detail = _('Discipline not found in the database.')
    default_code = 'discipline_not_found'

class NoTasksFoundException(APIException):
    status_code = 200
    default_detail = _('No tasks associated with the discipline.')
    default_code = 'no_tasks_found'