from django.urls import path
from . import views

urlpatterns = [
    path('', views.game, name='signup'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('assets/', views.assets, name='assets'),
    path('transactions/', views.transactions, name='transactions'),
    path('wallet/', views.wallet, name='wallet'),
    path('history/<slug:name>/', views.history, name='history'),
]
