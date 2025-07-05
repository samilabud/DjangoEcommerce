from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializer import OrderSerializer
from django.template import loader
from django.http import HttpResponse


class IsOwnerOrAdmin(IsAuthenticated):
    """
    Custom permission: allow if user is the order owner or is staff.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class   = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        # staff sees all, others see only their orders
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        # set user to request.user
        serializer.save(user=self.request.user)

def all_orders(request):
    template = loader.get_template('all_orders.html')
    context = {
        'orders': Order.objects.all()
    }
    return HttpResponse(template.render(context, request))