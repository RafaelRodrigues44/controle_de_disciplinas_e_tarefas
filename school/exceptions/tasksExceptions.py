from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

class NoTaskFoundException(APIException):
    """
    Custom exception to indicate that no tasks were found in the database.
    """

    def __init__(self):
        self.message = "No tasks found in the database."
        super().__init__(self.message)


class MissingRequiredFieldsException(APIException):
    def __init__(self, missing_fields):
        self.missing_fields = missing_fields
        super().__init__(f"Missing required fields: {', '.join(missing_fields)}")


