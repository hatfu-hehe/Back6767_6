import requests
from rest_framework.generics import CreateAPIView
from users.serializers import OAuthCodeSerializer
from rest_framework.response import Response
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
import os

class GoogleLoginAPIView(CreateAPIView):
    serializer_class = OAuthCodeSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data["code"]    #reuired "data"
        
        token_response = requests.post(
            url="https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
                "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                "redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI"),
                "grant_type": "authorization_code"
            },
        )
        
        token_data = token_response.json()
        access_token = token_data.get("access_token")       # we cah set a default value for access_token
        
        if not access_token:
            return Response({'error': token_data})
        
        user_info = request.get(
            url="https://www.googleapis.com/oauth2/v3/userinfo",
            params={"alt": "json"},
            header={"Authorization": f"Bearer {access_token}"}
        ).json()
        
        print("USER_INFO: ", user_info)
        
        email = user_info["email"]
        
        user, created = CustomUser.objects.get_or_create(email=email)
        
        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        
        return Response(
            {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }
        )