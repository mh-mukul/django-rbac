from rest_framework import status
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from apps.core.permissions import IsSuperUser

from apps.core.helpers import ResponseHelper
from apps.organization.models import Organization
from apps.organization.serializers import OrganizationSerializer, OrganizationCreateUpdateSerializer


class OrganizationListView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request):
        organizations = Organization.get_active().order_by('id')
        page = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        paginator = Paginator(organizations, limit)
        organizations = paginator.get_page(page)
        serializer = OrganizationSerializer(organizations, many=True)
        return self.paginated_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data,
            page=organizations.number,
            total_pages=paginator.num_pages,
            total_items=paginator.count
        )


class OrganizationCreateView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def post(self, request):
        serializer = OrganizationCreateUpdateSerializer(
            data=request.data, context={"request": request})
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


class OrganizationDetailView(APIView, ResponseHelper):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, pk):
        organization = Organization.get_by_id(pk)
        if not organization:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Organization not found",
                errors=[{"organization_id": "Object with this ID does not exist."}]
            )
        serializer = OrganizationSerializer(organization)
        return self.success_response(
            status_code=status.HTTP_200_OK,
            message="Success",
            data=serializer.data
        )

    def put(self, request, pk):
        organization = Organization.get_by_id(pk)
        if not organization:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Organization not found",
                errors=[{"organization_id": "Object with this ID does not exist."}]
            )
        serializer = OrganizationCreateUpdateSerializer(
            organization, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            resp_serializer = OrganizationSerializer(organization)
            return self.success_response(
                status_code=status.HTTP_200_OK,
                message="Organization updated successfully",
                data=resp_serializer.data
            )
        return self.error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Failed to update organization",
            errors=serializer.errors
        )

    def delete(self, request, pk):
        organization = Organization.get_by_id(pk)
        if not organization:
            return self.error_response(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Organization not found",
                errors=[{"organization_id": "Object with this ID does not exist."}]
            )
        organization.soft_delete()
        return self.success_response(
            status_code=status.HTTP_204_NO_CONTENT,
            message="Organization deleted successfully"
        )
