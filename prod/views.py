from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from django.forms import model_to_dict
from .serializers import (
    CategoryListSerializer, ReviewDetailsSerializer, ReviewListSerializer,
    ProductDetailsSerializer, CategoryDetailsSerializer, ProductListSerializer,
    ProductWithReviewsSerializer, CategoryWithCountSerializer,
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer,
)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        catego = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryDetailsSerializer(catego, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        catego.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        catego.name = serializer.validated_data.get('name')
        catego.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=CategoryDetailsSerializer(catego).data)


@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categ = Category.objects.all()
        list_ = CategoryListSerializer(categ, many=True).data
        return Response(status=status.HTTP_200_OK, data=list_)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')
        catego = Category.objects.create(name=name)
        return Response(data=CategoryDetailsSerializer(catego).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def prod_list_create_api_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        list_ = ProductListSerializer(product, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=list_
        )
    elif request.method == 'POST':
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


@api_view(['GET', 'PUT', 'DELETE'])
def prod_detail_api_view(request, id):
    try:
        prod = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductDetailsSerializer(prod, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        prod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
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


@api_view(['GET', 'POST'])
def rev_list_create_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        list_ = ReviewListSerializer(review, many=True).data
        return Response(
            status=status.HTTP_200_OK,
            data=list_
        )
    elif request.method == 'POST':
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


@api_view(['GET', 'PUT', 'DELETE'])
def rev_detail_api_view(request, id):
    try:
        rev = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewDetailsSerializer(rev, many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        rev.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
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