from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list_create_api_view),
    path('category/<int:id>/', views.category_detail_api_view),
    path('product/', views.prod_list_create_api_view),
    path('product/<int:id>/', views.prod_detail_api_view),
    path('api/v1/review/', views.rev_list_create_api_view),
    path('review/<int:id>/', views.rev_detail_api_view),
    path('products/reviews/', views.products_reviews_api_view),
    path('categories/count', views.category_list_with_count_api_view),
]
