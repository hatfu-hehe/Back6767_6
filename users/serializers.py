from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import CustomUser


class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserCreateSerializer(UserBaseSerializer):

    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise ValidationError('User already exists!')


class UserConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)