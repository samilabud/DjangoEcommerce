from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('PROCESSING','Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total      = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    @transaction.atomic
    def recalculate_total(self):
        """
        Sum up order items; wrap in a transaction to ensure
        consistency if multiple items are changing.
        """
        total = sum(item.line_total for item in self.items.all())
        self.total = total
        self.save(update_fields=['total'])


class OrderItem(models.Model):
    order     = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product   = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity  = models.PositiveIntegerField(default=1)
    unit_price= models.DecimalField(max_digits=10, decimal_places=2)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['order', 'product']]

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        # On create, capture the product's current price
        if not self.pk:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)
        # Recalculate the order total whenever an item is added/updated
        self.order.recalculate_total()
