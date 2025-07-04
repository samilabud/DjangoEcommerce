from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'price',
            'inventory',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
