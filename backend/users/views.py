from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .auth import ClerkAuthentication
from loguru import logger

@api_view(['GET'])
@authentication_classes([ClerkAuthentication])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    logger.info("This is an INFO message from who_am_i")
    user = request.user
    return Response({
        'id': user.clerk_id,
        'email': user.email,
    })