from rest_framework.response import Response


class ResponseHelper:
    def success_response(self, status_code, message, data=None):
        return Response({
            "status": status_code,
            "message": message,
            "data": data
        }, status=status_code)

    def error_response(self, status_code, message, errors: list = None):
        return Response({
            "status": status_code,
            "message": message,
            "errors": errors
        }, status=status_code)
