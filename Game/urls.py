from django.urls import path
from . import views, ajax

urlpatterns = [
    path('', views.game, name='signup'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('assets/', views.assets, name='assets'),
    path('transactions/', views.transactions, name='transactions'),
    path('wallet/', views.wallet, name='wallet'),
    path('history/<slug:name>/', views.history, name='history'),
    path('alarms/', views.alarms, name='my_alarms'),
    path('alarm/set/', views.set_alarm, name='set_alarm'),
    path('ranking/', views.ranking, name='ranking'),
    path('loan/set/', views.set_loan_offer, name='loan_offer'),
    path('loans/', views.get_all_loan_offers, name='all_loans'),
    path('loans/offered', views.get_offered_loans, name='offered_loans'),


    path('ajax/quote/<slug:name>/', ajax.ajax_quote, name='ajax_quote'),
    path('ajax/buy/', ajax.ajax_buy, name='ajax_buy'),
    path('ajax/sell/', ajax.ajax_sell, name='ajax_sell'),
]
