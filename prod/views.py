from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product, Category, Review
from .serializers import (
    CategoryListSerializer, ReviewDetailsSerializer, ReviewListSerializer,
    ProductDetailsSerializer, CategoryDetailsSerializer, ProductListSerializer,
    ProductWithReviewsSerializer, CategoryWithCountSerializer,
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer,
)
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailsSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')
        catego = Category.objects.create(name=name)
        return Response(data=CategoryDetailsSerializer(catego).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        catego = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        catego.name = serializer.validated_data.get('name')
        catego.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailsSerializer(catego).data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        title = serializer.validated_data.get('title')
        price = serializer.validated_data.get('price')
        description = serializer.validated_data.get('description')
        category_id = serializer.validated_data.get('category_id')

        prod = Product.objects.create(
            title=title,
            price=price,
            description=description,
            category_id=category_id
        )
        return Response(data=ProductDetailsSerializer(prod).data,
                         status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        prod = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        prod.title = serializer.validated_data.get('title')
        prod.price = serializer.validated_data.get('price')
        prod.description = serializer.validated_data.get('description')
        prod.category_id = serializer.validated_data.get('category_id')
        prod.save()
        return Response(status=status.HTTP_201_CREATED,
                         data=ProductDetailsSerializer(prod).data)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailsSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')

        rev = Review.objects.create(
            text=text,
            stars=stars,
            product_id=product_id
        )
        return Response(data=ReviewDetailsSerializer(rev).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        rev = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        rev.text = serializer.validated_data.get('text')
        rev.stars = serializer.validated_data.get('stars')
        rev.product_id = serializer.validated_data.get('product_id')
        rev.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewDetailsSerializer(rev).data)


@api_view(['GET'])
def products_reviews_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    data = ProductWithReviewsSerializer(products, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)


@api_view(['GET'])
def category_list_with_count_api_view(request):
    categories = Category.objects.prefetch_related('products').all()
    data = CategoryWithCountSerializer(categories, many=True).data
    return Response(status=status.HTTP_200_OK, data=data)