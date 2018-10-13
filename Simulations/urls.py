from django.urls import path
from . import responses


urlpatterns = [
    path('getAvailableAssets/', responses.get_available_assets, name='getAvailableAssets'),
    path('getAssetMarketPrice/<slug:name>', responses.get_asset_marketprice, name='getAssetMarketPrice')
]
