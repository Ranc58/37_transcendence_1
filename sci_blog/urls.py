from django.contrib import admin
from django.urls import path, include
from users_app.urls import urlpatterns as users_app_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users_app.urls'))
]
