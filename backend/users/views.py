from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def who_am_i(request):
    # ClerkMiddleware has already set request.user
    user = request.user
    return JsonResponse({
        'id': user.clerk_id,
        'email': user.email,
    })
