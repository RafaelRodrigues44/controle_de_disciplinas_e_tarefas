from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class DisciplineValidationException(APIException):
    status_code = 400
    default_detail = _('This field is required.')
    default_code = 'discipline_validation_error'
