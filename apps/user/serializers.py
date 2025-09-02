"""
Serializers for the users app.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.authorization.serializers import RoleSerializer
from apps.organization.serializers import OrganizationSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    role = RoleSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'email', 'is_admin',
                  'is_active', 'organization', 'role', 'last_login', 'image']
        read_only_fields = ['id', 'last_login']

    def get_image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users.
    """
    password = serializers.CharField(write_only=True, required=True, style={
                                     'input_type': 'password'})
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['name', 'mobile', 'email', 'password', 'password_confirm',
                  'is_admin', 'is_active', 'role', 'image']

    def validate(self, data):
        """
        Check that the passwords match.
        """
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."})
        # Check if role belongs to the same organization as the user creating it
        request = self.context.get("request")
        user = request.user if request else None
        role = data.get('role')
        if role and user and not user.is_superuser:
            if role.organization != user.organization:
                raise serializers.ValidationError(
                    {"role": "Invalid role selected."})

        return data

    def create(self, validated_data):
        """
        Create and return a new user with encrypted password.
        """
        request = self.context.get("request")
        user = request.user if request else None
        validated_data['organization'] = user.organization if user else None
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating users.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'is_admin', 'is_active', 'role', 'image']

    def validate(self, attrs):
        # Check if role belongs to the same organization as the user updating it
        request = self.context.get("request")
        user = request.user if request else None
        role = attrs.get('role')
        if role and user and not user.is_superuser:
            if role.organization != user.organization:
                raise serializers.ValidationError(
                    {"role": "Invalid role selected."})
        return attrs

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(
        required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError(
                {"new_password_confirm": "New passwords do not match."})
        return data
