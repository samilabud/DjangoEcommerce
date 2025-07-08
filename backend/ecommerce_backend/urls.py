from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from products.views import ProductViewSet
from orders.views   import OrderViewSet
from orders.urls    import urlpartners as order_urls
from products.urls  import urlpartners as product_urls

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders',   OrderViewSet,   basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/me/', include('users.urls')),
    path('api/v1/', include(router.urls)),
    path('orders/', include(order_urls)),
    path('products/', include(product_urls)),
]

if settings.DEBUG:
    print('DEBUG MODE')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # media/products/2025/07/04/home-1_CFJkrXv.jpg
else:
    print('PRODUCTION MODE')