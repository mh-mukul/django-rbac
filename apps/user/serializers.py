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

    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'email', 'is_admin',
                  'is_active', 'organization', 'role', 'last_login']
        read_only_fields = ['id', 'last_login']


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
                  'is_admin', 'is_active', 'role']

    def validate(self, data):
        """
        Check that the passwords match.
        """
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."})
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
        fields = ['name', 'email', 'is_admin', 'is_active', 'role']


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
