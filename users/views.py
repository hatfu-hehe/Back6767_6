from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.create_user(
        username=username,
        password=password,
        is_active=False
    )
    confirm_code = ConfirmCode.objects.create(user=user)
    print(f'Code for {username}: {confirm_code.code}')

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


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