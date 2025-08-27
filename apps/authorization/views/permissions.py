from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsSuperUser

from apps.core.helpers import ResponseHelper
from apps.authorization.models import Permission
from apps.authorization.serializers import PermissionSerializer, PermissionCreateUpdateSerializer


class PermissionListCreateView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        permissions = Permission.get_active().order_by('id')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(permissions, limit)
        permissions = paginator.get_page(page)
        serializer = PermissionSerializer(permissions, many=True)
        return self.paginated_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data,
            page=permissions.number,
            total_pages=paginator.num_pages,
            total_items=paginator.count
        )

    def post(self, request):
        serializer = PermissionCreateUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                errors=serializer.errors
            )
        permission = serializer.save()
        return self.success_response(
            status_code=status.HTTP_201_CREATED,
            message="Permission created successfully",
            data=PermissionSerializer(permission).data
        )


class PermissionDetailsView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, pk):
        permission = Permission.get_by_id(pk)
        if not permission:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Permission not found",
                errors={"id": ["Permission with this ID does not exist."]}
            )
        serializer = PermissionSerializer(permission)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )

    def put(self, request, pk):
        permission = Permission.get_by_id(pk)
        if not permission:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Permission not found",
                errors={"id": ["Permission with this ID does not exist."]}
            )
        serializer = PermissionCreateUpdateSerializer(
            permission, data=request.data, partial=True)
        if not serializer.is_valid():
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                errors=serializer.errors
            )
        permission = serializer.save()
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Permission updated successfully",
            data=PermissionSerializer(permission).data
        )

    def delete(self, request, pk):
        permission = Permission.get_by_id(pk)
        if not permission:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Permission not found",
                errors={"id": ["Permission with this ID does not exist."]}
            )
        permission.soft_delete()
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Permission deleted successfully"
        )
