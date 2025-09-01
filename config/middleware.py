import logging
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class CustomExceptionMiddleware:
    """
    Custom middleware to handle unhandled exceptions and return
    a structured JSON response for Django Rest Framework applications.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception as exc:
            # Log the error with traceback
            logger.error("Unhandled exception: %s", str(exc), exc_info=True)

            response_data = {
                "status": 500,
                "message": "Something went wrong",
                "data": None
            }

            return Response(response_data, status=500)
