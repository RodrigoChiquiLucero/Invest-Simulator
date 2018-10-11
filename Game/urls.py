from django.urls import path
from . import views


urlpatterns = [
    path('', views.game, name='signup'),
    path('assets/', views.assets, name='assets'),
]
