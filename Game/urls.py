from django.urls import path
from . import views

urlpatterns = [
    path('', views.game, name='signup'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('assets/', views.assets, name='assets'),
    path('transactions/', views.transactions, name='transactions'),
    path('wallet/', views.wallet, name='wallet'),
    path('history/<slug:name>/', views.history, name='history'),
    path('alarm/set/', views.set_alarm, name='set_alarm'),

    path('ajax/quote/<slug:name>/', views.ajax_quote, name='ajax_quote'),
    path('ajax/buy/', views.ajax_buy, name='ajax_buy'),
    path('ajax/sell/', views.ajax_sell, name='ajax_sell'),
]
