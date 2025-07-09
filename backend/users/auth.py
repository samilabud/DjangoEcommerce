# users/auth.py
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions
from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from loguru import logger
import jwt

class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            print("Missing Bearer token")
            return None

        # token = auth.split()[1]

        sdk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

        opts = AuthenticateRequestOptions(
            authorized_parties=settings.CLERK_AUTHORIZED_PARTIES 
        )
        state = sdk.authenticate_request(request, opts)

        logger.info(f"Clerk auth: signed_in={state.is_signed_in} reason={state.reason}")

        if not state.is_signed_in:
            raise exceptions.AuthenticationFailed("Invalid or expired Clerk token")

        payload = state.payload
        if not payload:
            raise exceptions.AuthenticationFailed("Invalid Clerk token")
        clerk_id = payload["sub"]

        User = get_user_model()
        user, _ = User.objects.get_or_create(
            clerk_id=clerk_id,
            defaults={
                "email": payload.get("email", ""),
                "username": payload.get("email", ""),
            },
        )
        return (user, None)

