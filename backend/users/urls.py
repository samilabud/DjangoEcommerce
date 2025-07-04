from django.urls import path
from users.views import who_am_i

urlpatterns = [
    path('', who_am_i, name='who_am_i'),
]
