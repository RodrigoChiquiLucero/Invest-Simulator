from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('user/', include('User.urls')),
    path('game/', include('Game.urls')),
    path('tests/', include('Simulations.urls')),
]
