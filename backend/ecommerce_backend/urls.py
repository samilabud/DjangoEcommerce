from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet
from orders.views   import OrderViewSet
from orders.urls    import urlpartners as order_urls

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders',   OrderViewSet,   basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/me/', include('users.urls')),  # your existing auth endpoint
    path('api/v1/', include(router.urls)),
    path('orders/', include(order_urls)),
]
