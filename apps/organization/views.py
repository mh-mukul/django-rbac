from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsAdminUser, IsSuperUser

from apps.core.helpers import ResponseHelper
from apps.organization.models import Organization
from apps.organization.serializers import OrganizationSerializer, OrganizationCreateUpdateSerializer


class OrganizationListView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def get(self, request):
        organizations = Organization.objects.all()
        serializer = OrganizationSerializer(organizations, many=True)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )


class OrganizationDetailView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def get(self, request, pk):
        organization = Organization.objects.get(pk=pk)
        serializer = OrganizationSerializer(organization)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )

    def put(self, request, pk):
        organization = Organization.objects.get(pk=pk)
        serializer = OrganizationCreateUpdateSerializer(
            organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(
                status_code=status.HTTP_200_OK,
                message="Organization updated successfully",
                data=serializer.data
            )
        return self.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Failed to update organization",
            errors=serializer.errors
        )

    def delete(self, request, pk):
        organization = Organization.objects.get(pk=pk)
        organization.delete()
        return self.success_response(
            status_code=status.HTTP_204_NO_CONTENT,
            message="Organization deleted successfully"
        )


class OrganizationCreateView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def post(self, request):
        serializer = OrganizationCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            organization = serializer.save()
            return self.success_response(
                status_code=status.HTTP_201_CREATED,
                message="Organization created successfully",
                data=OrganizationSerializer(organization).data
            )
        return self.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Failed to create organization",
            errors=serializer.errors
        )
