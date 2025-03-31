from rest_framework import serializers
from .models import Category, Product, Contact, Newsletter, Order
from .models import *
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'description', 'slug']

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ['text']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url', 'alt_text']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    features = FeatureSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'features', 'images', 
                  'category', 'stock', 'rating', 'reviews', 'is_featured', 'color']
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['created_at']

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'