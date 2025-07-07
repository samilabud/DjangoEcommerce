from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from django.http import HttpResponse
from django.template import loader

class ProductViewSet(viewsets.ModelViewSet):
    queryset         = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


def ProductList(request):
    template = loader.get_template('product_list.html')
    context = {
        'products': Product.objects.all()
    }
    return HttpResponse(template.render(context, request))

def ProductDetail(request, slug):
    template = loader.get_template('product_detail.html')
    context = {
        'product': Product.objects.get(slug=slug)
    }
    return HttpResponse(template.render(context, request))