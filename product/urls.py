from django.contrib import admin
from django.urls import path, include
from . import swagger
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import CustomTokenObtainPairView
from users.google_oauth import GoogleLoginAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/prod/', include('prod.urls')),
    path('api/v1/users/', include('users.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('google-login', GoogleLoginAPIView.as_view())
    # path('api/v1/category/', views.category_list_create_api_view),
    # path('api/v1/category/<int:id>/', views.category_detail_api_view),
    # path('api/v1/product/', views.prod_list_create_api_view),
    # path('api/v1/product/<int:id>/', views.prod_detail_api_view),
    # path('api/v1/review/', views.rev_list_create_api_view),
    # path('api/v1/review/<int:id>/', views.rev_detail_api_view),
    # path('api/v1/products/reviews/', views.products_reviews_api_view),
    # path('api/v1/categories/count', views.category_list_with_count_api_view),
]

urlpatterns += swagger.urlpatterns