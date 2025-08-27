from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsSuperUser

from apps.core.helpers import ResponseHelper
from apps.authorization.models import Module
from apps.authorization.serializers import ModuleSerializer


class ModuleListCreateView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        modules = Module.get_active().order_by('id')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(modules, limit)
        modules = paginator.get_page(page)
        serializer = ModuleSerializer(modules, many=True)
        return self.paginated_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data,
            page=modules.number,
            total_pages=paginator.num_pages,
            total_items=paginator.count
        )

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                errors=serializer.errors
            )
        module = serializer.save()
        return self.success_response(
            status_code=status.HTTP_201_CREATED,
            message="Module created successfully",
            data=ModuleSerializer(module).data
        )


class ModuleDetailsView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, pk):
        module = Module.get_by_id(pk)
        if not module:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Module not found",
                errors={"id": ["Module with this ID does not exist."]}
            )
        serializer = ModuleSerializer(module)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )

    def put(self, request, pk):
        module = Module.get_by_id(pk)
        if not module:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Module not found",
                errors={"id": ["Module with this ID does not exist."]}
            )
        serializer = ModuleSerializer(module, data=request.data, partial=True)
        if not serializer.is_valid():
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                errors=serializer.errors
            )
        module = serializer.save()
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Module updated successfully",
            data=ModuleSerializer(module).data
        )

    def delete(self, request, pk):
        module = Module.get_by_id(pk)
        if not module:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Module not found",
                errors={"id": ["Module with this ID does not exist."]}
            )
        module.soft_delete()
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Module deleted successfully"
        )
