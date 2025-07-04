from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('unit_price', 'line_total')
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display    = ('id', 'user', 'status', 'total', 'created_at')
    list_filter     = ('status',)
    inlines         = [OrderItemInline]
    readonly_fields = ('total',)
