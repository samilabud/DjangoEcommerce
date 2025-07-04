from django.contrib import admin
from .models import Product
from loguru import logger

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'price', 'inventory', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        logger.info(f"Product '{obj.name}' has been saved.")
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        logger.info(f"Product '{obj.name}' has been deleted.")
    
