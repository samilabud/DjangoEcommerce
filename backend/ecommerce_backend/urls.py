from django.contrib import admin
from django.urls import  path
from users.views import who_am_i

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/me/', who_am_i, name='who_am_i'),
]
