from django.urls import path
from . import responses

urlpatterns = [
    path('getAvailableAssets/', responses.get_available_assets,
         name='getAvailableAssets'),
    path('getAssetMarketPrice/<slug:name>', responses.get_asset_marketprice,
         name='getAssetMarketPrice'),
    path('getAssetHistory/<slug:name>/<slug:start_date>/<slug:end_date>',
         responses.get_asset_history, name='getAssetHistory')
]
