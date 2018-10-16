from django.urls import path
from . import views


urlpatterns = [
    path('', views.game, name='signup'),
    path('assets/', views.assets, name='assets'),
    path('wallet/', views.wallet, name='wallet'),
    path('loggedin/', views.loggedin, name='loggedin'),
]
