from django.urls import path
from . import views

urlpatterns = [
    path('', views.game, name='signup'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('assets/', views.assets, name='assets'),
    path('wallet/', views.wallet, name='wallet'),
    path('history/<slug:name>/<slug:start>/<slug:end>', views.history,
         name='history'),
]
