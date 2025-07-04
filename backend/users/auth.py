# users/auth.py
from rest_framework import authentication, exceptions
from clerk import Clerk  # from clerk-sdk
from loguru import logger

class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        logger.info("This is an INFO message from authenticate")
        auth = request.headers.get('Authorization', '')
        if not auth.startswith('Bearer '):
            return None
        token = auth.split()[1]
        try:
            payload = Clerk.jwt.verify(token)       # verify signature
            clerk_id = payload['sub']
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid Clerk token')

        # Lookup or sync the user in your DB
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, _ = User.objects.get_or_create(clerk_id=clerk_id, defaults={
            'email': payload.get('email'),
            'username': payload.get('email'),
        })
        return (user, None)