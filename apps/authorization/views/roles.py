from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsAdminUser, IsSuperUser

from apps.core.helpers import ResponseHelper
from apps.authorization.models import Role, RolePermission
from apps.authorization.serializers import RoleSerializer, RoleCreateUpdateSerializer


class RoleListCreateView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def get(self, request):
        roles = Role.get_all().order_by('id')
        if not request.user.is_superuser:
            roles = roles.filter(organization=request.user.organization)
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(roles, limit)
        roles = paginator.get_page(page)
        serializer = RoleSerializer(roles, many=True)
        return self.paginated_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data,
            page=roles.number,
            total_pages=paginator.num_pages,
            total_items=paginator.count
        )

    def post(self, request):
        serializer = RoleCreateUpdateSerializer(
            data=request.data, context={'request': request})
        if not serializer.is_valid():
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                errors=serializer.errors
            )
        role = serializer.save()
        return self.success_response(
            status_code=status.HTTP_201_CREATED,
            message="Role created successfully",
            data=RoleSerializer(role).data
        )


class RoleDetailsView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def get(self, request, pk):
        if request.user.is_superuser:
            role = Role.get_by_id(pk)
        else:
            role = Role.objects.filter(
                id=pk, organization=request.user.organization).first()
        if not role:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Role not found",
                errors={"id": ["Role with this ID does not exist."]}
            )
        serializer = RoleSerializer(role)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )

    def put(self, request, pk):
        if request.user.is_superuser:
            role = Role.get_by_id(pk)
        else:
            role = Role.objects.filter(
                id=pk, organization=request.user.organization).first()
        if not role:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Role not found",
                errors={"id": ["Role with this ID does not exist."]}
            )
        serializer = RoleCreateUpdateSerializer(
            role, data=request.data, partial=True, context={'request': request})
        if not serializer.is_valid():
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Invalid data",
                errors=serializer.errors
            )
        role = serializer.save()
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Role updated successfully",
            data=RoleSerializer(role).data
        )

    def delete(self, request, pk):
        if request.user.is_superuser:
            role = Role.get_by_id(pk)
        else:
            role = Role.objects.filter(
                id=pk, organization=request.user.organization).first()
        if not role:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Role not found",
                errors={"id": ["Role with this ID does not exist."]}
            )
        role.soft_delete()
        RolePermission.objects.filter(role=role, is_deleted=False).update(
            is_active=False, is_deleted=True)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Role deleted successfully"
        )
