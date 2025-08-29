import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.core.helpers import ResponseHelper
from apps.authentication.serializers import LogoutSerializer

logger = logging.getLogger('authentication')


class UserLoginView(TokenObtainPairView, ResponseHelper):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if not response.status_code == 200:
                return self.error_response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Unable to verify credentials",
                    errors={
                        "detail": "No active account found with the given credentials"}
                )
            user_instance = User.objects.filter(
                mobile=request.data.get('mobile'), is_active=True, is_deleted=False).first()
            if not user_instance:
                return self.error_response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Unable to verify credentials",
                    errors={
                        "detail": "No active account found with the given credentials"}
                )
            custom_response_data = {
                "access_token": response.data.get("access"),
                "refresh_token": response.data.get("refresh"),
                "token_type": "bearer",
                "user": {
                    "id": user_instance.id,
                    "name": user_instance.name,
                    "email": user_instance.email,
                    "mobile": user_instance.mobile,
                    "is_password_reset_required": user_instance.is_password_reset_required,
                    "is_superuser": user_instance.is_superuser,
                    "is_staff": user_instance.is_staff,
                    "organization": {
                        "id": user_instance.organization.id,
                        "name": user_instance.organization.name
                    } if user_instance.organization else None
                },
            }
            return self.success_response(
                status_code=status.HTTP_200_OK,
                message="Successfully Logged In",
                data=custom_response_data
            )

        except Exception as e:
            logger.error("Error during user login", exc_info=True,
                         extra={"mobile": request.data.get("mobile"), "error": str(e)})
            return self.error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Something went wrong",
                errors=[str(e)]
            )


class UserLogoutView(APIView, ResponseHelper):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            try:
                # Blacklist the refresh token
                refresh_token_obj = RefreshToken(
                    serializer.data.get('refresh_token'))
                refresh_token_obj.blacklist()

                return self.success_response(
                    status_code=status.HTTP_200_OK,
                    message="Successfully Logged Out",
                    data=None
                )
            except TokenError as e:
                logger.error("Token error during logout", exc_info=True,
                             extra={"user_id": request.user.id, "error": str(e)})
                return self.error_response(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    message="Token Error",
                    errors=[str(e)]
                )
            except Exception as e:
                logger.error("Error during user logout", exc_info=True,
                             extra={"user_id": request.user.id, "error": str(e)})
                return self.error_response(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    message="Something went wrong",
                    errors=[str(e)]
                )
        else:
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Unable to Logout",
                errors=serializer.errors
            )


class RefreshTokenView(APIView, ResponseHelper):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return self.error_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Refresh token is required",
                errors=[{"refresh_token": "This field is required."}]
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            user_instance = User.get_by_id(refresh.payload.get('user_id'))
            if not user_instance:
                return self.error_response(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="User not found",
                    errors=[
                        {"detail": "No active account found with the given credentials"}]
                )
            custom_response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": {
                    "id": user_instance.id,
                    "name": user_instance.name,
                    "email": user_instance.email,
                    "mobile": user_instance.mobile,
                    "is_password_reset_required": user_instance.is_password_reset_required,
                    "is_superuser": user_instance.is_superuser,
                    "is_staff": user_instance.is_staff,
                    "organization": {
                        "id": user_instance.organization.id,
                        "name": user_instance.organization.name
                    } if user_instance.organization else None
                },
            }
            return self.success_response(
                status_code=status.HTTP_200_OK,
                message="Success",
                data=custom_response_data
            )
        except Exception as e:
            logger.error("Error during token refresh", exc_info=True,
                         extra={"error": str(e)})
            return self.error_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message="Something went wrong",
                errors=[str(e)]
            )
