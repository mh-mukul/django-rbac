from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.core.helpers import ResponseHelper
from apps.authentication.serializers import LogoutSerializer


class UserLoginView(TokenObtainPairView, ResponseHelper):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == 200:
                user_instance = User.objects.get(
                    mobile=request.data.get('mobile'))
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
                    },
                }
                return self.success_response(200, "Successfully Logged In", data=custom_response_data)
            return self.error_response(401, "Unable to verify credentials", errors=["Invalid mobile or password"])

        except Exception as e:
            return self.error_response(
                500, "Internal Server Error", errors=[str(e)]
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

                return self.success_response(200, "Successfully Logged Out", None)
            except TokenError as e:
                return self.error_response(400, "Token Error", errors=[str(e)])
            except Exception as e:
                return self.error_response(400, "Logout Failed", errors=[str(e)])
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
            return self.error_response(400, 'Invalid Parameters', errors=[{"refresh_token": "This field is required."}])

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            user = User.objects.get(id=refresh.payload.get('user_id'))
            custom_response_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "mobile": user.mobile,
                }
            }
            return self.success_response(200, 'Token Refreshed', data=custom_response_data)
        except Exception as e:
            return self.error_response(401, 'Token Refresh Failed', errors=[str(e)])
