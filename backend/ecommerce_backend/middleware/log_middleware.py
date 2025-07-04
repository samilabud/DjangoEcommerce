import uuid
from loguru import logger

class LogContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = str(uuid.uuid4())
        # now that AuthenticationMiddleware has run, request.user is authoritative
        user = getattr(request, "user", None)
        # if ClerkAuthentication set clerk_id, grab it; otherwise fall back to user.id if you want
        user_id = getattr(user, "clerk_id", None) or getattr(user, "id", None)

        with logger.contextualize(request_id=request_id, user_id=user_id):
            response = self.get_response(request)
            return response
