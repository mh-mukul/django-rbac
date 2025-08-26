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

    def paginated_response(self, status_code, message, data, page=1, total_pages=1, total_items=0):
        return Response({
            "status": status_code,
            "message": message,
            "data": data,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_items": total_items
            }
        }, status=status_code)
