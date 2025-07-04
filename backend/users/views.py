from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .auth import ClerkAuthentication

@api_view(['GET'])
@authentication_classes([ClerkAuthentication])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    user = request.user
    return Response({
        'id': user.clerk_id,
        'email': user.email,
    })