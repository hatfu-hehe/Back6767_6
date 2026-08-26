from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category, Review
from django.forms import model_to_dict
from .serializers import CategoryListSerializer, ReviewDetailsSerializer, ReviewListSerializer, ProductDetailsSerializer, CategoryDetailsSerializer, ProductListSerializer, ProductWithReviewsSerializer, CategoryWithCountSerializer

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        catego = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategoryDetailsSerializer(catego, many=False).data
    return Response(data=data)

@api_view(['GET'])
def category_list_api_view(request):
    categ = Category.objects.all()
    list_ = CategoryListSerializer(categ, many=True).data
    return Response(status=status.HTTP_200_OK, data=list_)
    
@api_view(['GET'])
def prod_list_api_view(request):
    product = Product.objects.all()
    list_ = ProductListSerializer(product, many=True).data
    for i in product:
        list_.append(model_to_dict(i))
    return Response(
        status=status.HTTP_200_OK,
        data=list_
    )
    
@api_view(['GET'])
def prod_detail_api_view(request, id):
    try:
        prod = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailsSerializer(prod, many=False).data
    return Response(data=data)

@api_view(['GET'])
def rev_list_api_view(request):
    review = Review.objects.all()
    list_ = ReviewListSerializer(review, many=True).data
    for i in review:
        list_.append(model_to_dict(i))
    return Response(
        status=status.HTTP_200_OK,
        data=list_
    )
    
@api_view(['GET'])
def rev_detail_api_view(request, id):
    try:
        rev = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewDetailsSerializer(rev, many=False).data
    return Response(data=data)

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