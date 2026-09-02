
from django.contrib import admin
from django.urls import path
from prod import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/category/', views.category_list_create_api_view),
    path('api/v1/category/<int:id>/', views.category_detail_api_view),
    path('api/v1/product/', views.prod_list_create_api_view),
    path('api/v1/product/<int:id>/', views.prod_detail_api_view),
    path('api/v1/review/', views.rev_list_create_api_view),
    path('api/v1/review/<int:id>/', views.rev_detail_api_view),
    path('api/v1/products/reviews/', views.products_reviews_api_view),
    path('api/v1/categories/count', views.category_list_with_count_api_view),
]
