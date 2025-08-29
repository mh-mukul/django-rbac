from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsSuperUser

from apps.core.helpers import ResponseHelper
from apps.user.models import User
from apps.user.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


class UserListCreateView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        users = User.get_all().order_by('-id')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(users, limit)
        users = paginator.get_page(page)
        serializer = UserSerializer(users, many=True)
        return self.paginated_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data,
            page=users.number,
            total_pages=paginator.num_pages,
            total_items=paginator.count
        )

    def post(self, request):
        serializer = UserCreateSerializer(
            data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            return self.success_response(
                status_code=status.HTTP_201_CREATED,
                message="User created successfully",
                data=UserSerializer(user).data
            )
        return self.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Failed to create user",
            errors=serializer.errors
        )


class UserDetailView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, pk):
        user = User.get_by_id(pk)
        if not user:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                errors=[{"user_id": "Object with this ID does not exist."}]
            )
        serializer = UserSerializer(user)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )

    def put(self, request, pk):
        user = User.get_by_id(pk)
        if not user:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                errors=[{"user_id": "Object with this ID does not exist."}]
            )
        serializer = UserUpdateSerializer(
            user, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            user = serializer.save()
            return self.success_response(
                status_code=status.HTTP_200_OK,
                message="User updated successfully",
                data=UserSerializer(user).data
            )
        return self.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Failed to update user",
            errors=serializer.errors
        )

    def delete(self, request, pk):
        user = User.get_by_id(pk)
        if not user:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                errors=[{"user_id": "Object with this ID does not exist."}]
            )
        user.soft_delete()
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="User deleted successfully"
        )
