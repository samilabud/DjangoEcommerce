from django.urls import path
from .views import all_orders, order_details, main

urlpartners = [
    path('', main, name='main', ),
    path('all_orders', all_orders, name='all_orders', ),
    path('order_detail/<int:orderid>', order_details, name='order-detail', ),
]