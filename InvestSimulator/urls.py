from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('user/', include('User.urls')),
    path('game/', include('Game.urls')),
    path('tests/', include('Simulations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
