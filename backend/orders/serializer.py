from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=ProductSerializer.Meta.model.objects.all(), source='product'
    )

    class Meta:
        model  = OrderItem
        fields = [
            'id',
            'product',
            'product_id',
            'quantity',
            'unit_price',
            'line_total',
            'created_at',
        ]
        read_only_fields = ['id', 'unit_price', 'line_total', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model  = Order
        fields = [
            'id',
            'user',
            'status',
            'total',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'total', 'created_at', 'updated_at']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # user comes from request context
        order = Order.objects.create(user=self.context['request'].user, **validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order

    def update(self, instance, validated_data):
        # only allow status change or item qty changes
        items_data = validated_data.pop('items', None)
        if 'status' in validated_data:
            instance.status = validated_data['status']
            instance.save(update_fields=['status'])
        if items_data is not None:
            # rudimentary: clear & recreate
            instance.items.all().delete()
            for item in items_data:
                OrderItem.objects.create(order=instance, **item)
        return instance
