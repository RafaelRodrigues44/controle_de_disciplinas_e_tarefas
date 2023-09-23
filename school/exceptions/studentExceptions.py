from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class NoStudentsFoundException(APIException):
    status_code = 200
    default_detail = _('Have not students in database.')
    default_code = 'no_students_found'


class EmptyFieldsException(APIException):
    status_code = 400
    default_code = 'empty_fields'

    def __init__(self, fields):
        self.fields = fields
        self.detail = 'The following fields must be completed: {}.'.format(', '.join(fields))

class StudentNotFoundException(APIException):
    status_code = 404
    default_detail = _('Student not found.')
    default_code = 'student_not_found'