# users/auth.py
from django.conf import settings
from .models import User
from rest_framework import authentication, exceptions
from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from loguru import logger

class ClerkAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            print("Missing Bearer token")
            return None

        # token = auth.split()[1]

        sdk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
        user_details = sdk.users.list()
        
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
        email = payload.get("email", "")
        clerk_user = next(
            (u for u in user_details or [] if u.id == clerk_id),
            None
        )
        if clerk_user and clerk_user.email_addresses:
            email = clerk_user.email_addresses[0].email_address
        else:
            raise exceptions.AuthenticationFailed("No email found for Clerk user")
        
        try:
            user = User.objects.get(clerk_id=clerk_id)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=email)
                user.clerk_id = clerk_id
                user.save(update_fields=["clerk_id"])
            except User.DoesNotExist:
                user = User.objects.create(
                    username=email,
                    email=email,
                    clerk_id=clerk_id,
                )
        return (user, None)

