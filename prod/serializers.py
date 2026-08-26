from rest_framework import serializers
from .models import Product, Category, Review

class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
        # exclude = ['id']
        

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class ReviewDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews', 'rating']

    def get_rating(self, product):
        reviews = product.reviews.all()
        if not reviews:
            return None
        return round(sum(r.stars for r in reviews) / len(reviews), 2)


class CategoryWithCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, category):
        return category.products.count()