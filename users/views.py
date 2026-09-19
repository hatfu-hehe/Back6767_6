from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from .models import ConfirmCode, CustomUser


@swagger_auto_schema(method='post', request_body=UserCreateSerializer)
@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    password = request.data.get('password')
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        is_active=False
    )
    confirm_code = ConfirmCode.objects.create(user=user)
    print(f'Code for {email}: {confirm_code.code}')

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})


@swagger_auto_schema(method='post', request_body=UserAuthSerializer)
@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(method='post', request_body=UserConfirmSerializer)
@api_view(['POST'])
def confirm_api_view(request):
    serializer = UserConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user_id = serializer.validated_data['user_id']
    code = serializer.validated_data['code']

    try:
        confirm_code = ConfirmCode.objects.get(user_id=user_id, code=code)
    except ConfirmCode.DoesNotExist:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Wrong code numbers'}
        )

    user = confirm_code.user
    user.is_active = True
    user.save()
    confirm_code.delete()

    return Response(data={'detail': 'Success'})