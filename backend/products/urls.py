from .views import ProductList, ProductDetail
from django.urls import path

urlpartners = [
    path('', ProductList, name='products'),
    path('<slug:slug>', ProductDetail, name='product_detail'),
]