from django.urls import path
from .views import all_orders

urlpartners = [
    path('all_orders', all_orders, name='all_orders', ),
]