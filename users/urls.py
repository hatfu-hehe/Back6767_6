from django.urls import path
from . import views
from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('registration/', views.registration_api_view),
    path('auth/', views.authorization_api_view),
    path('confirm/', views.confirm_api_view),
    path('google-login', GoogleLoginAPIView.as_view())
]