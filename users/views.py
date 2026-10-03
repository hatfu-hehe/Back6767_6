from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema

from .serializers import UserCreateSerializer, UserAuthSerializer, UserConfirmSerializer, CustomTokenObtainPairSerializer
from .models import CustomUser

from rest_framework_simplejwt.views import TokenObtainPairView

from common.validators import validate_age
from .codes import save_code, check_code


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



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
    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        is_active=False
    )
    code = save_code(user.id)
    print(f'Code for {email}: {code}')

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

    if not check_code(user_id, code):
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={'error': 'Wrong code numbers'}
        )

    user = CustomUser.objects.get(id=user_id)
    user.is_active = True
    user.save()

    return Response(data={'detail': 'Success'})