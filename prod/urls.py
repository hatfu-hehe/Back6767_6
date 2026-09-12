from django.urls import path
from . import views
from .constants import LIST_CREATE, DETAIL

urlpatterns = [
    path('category/', views.CategoryViewSet.as_view(LIST_CREATE)),
    path('category/<int:id>/', views.CategoryViewSet.as_view(DETAIL)),
    path('product/', views.ProductViewSet.as_view(LIST_CREATE)),
    path('product/<int:id>/', views.ProductViewSet.as_view(DETAIL)),
    path('api/v1/review/', views.ReviewViewSet.as_view(LIST_CREATE)),
    path('review/<int:id>/', views.ReviewViewSet.as_view(DETAIL)),
    path('products/reviews/', views.products_reviews_api_view),
    path('categories/count', views.category_list_with_count_api_view),
]
