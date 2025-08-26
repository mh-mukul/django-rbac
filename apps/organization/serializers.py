from rest_framework import serializers
from apps.organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "is_active", "created_at"]


class OrganizationCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        validated_data['is_active'] = True
        return Organization.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        validated_data['updated_by'] = user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
