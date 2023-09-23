from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class DisciplineValidationException(APIException):
    status_code = 400
    default_detail = _('This field is required.')
    default_code = 'discipline_validation_error'


class DisciplineNotFoundException(APIException):
    status_code = 404
    default_code = 'discipline_not_found'
    default_detail = 'Discipline not found.'

class NoDisciplinesFoundException(APIException):
    status_code = 404
    default_code = 'no_disciplines_found'
    default_detail = 'Database has no disciplines found.'

class DisciplineNotFoundException(APIException):
    status_code = 404
    default_code = 'discipline_not_found'
    default_detail = 'Discipline not found.'