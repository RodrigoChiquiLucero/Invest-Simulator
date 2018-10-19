import urllib3.request
import json
import datetime as dt
from urllib3 import exceptions as urlex

DATE_FORMAT = '%Y-%m-%d'


def str_to_date(strdate):
    return dt.datetime.strptime(strdate, DATE_FORMAT)


class AssetComunication:
    GET_ASSETS = "getAvailableAssets/"
    GET_QUOTE = "getAssetMarketPrice/"
    GET_HISTORY = "getAssetHistory/"

    def __init__(self, url):
        self.API_URL = url

    @staticmethod
    def has_quote(asset):
        return asset.buy != -1 and asset.sell != -1

    @staticmethod
    def url_to_json(url):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        http = urllib3.PoolManager()
        try:
            res = http.request('GET', url)
            if res.status == 200:
                return json.loads(res.data.decode())
            else:
                return 0
        except urlex.MaxRetryError:
            return 0

    def get_asset_names(self):
        from Game.models import Asset
        url = self.API_URL + self.GET_ASSETS
        json_assets = self.url_to_json(url)
        asset_list = []
        try:
            if json_assets != 0:
                json_assets = json_assets['availableAssets']
                for a in json_assets:
                    asset = Asset(name=a['name'], type=a['type'])
                    asset_list.append(asset)
                return asset_list
        except KeyError:
            # rollback
            asset_list = []
        finally:
            return asset_list

    def get_asset_quote(self, asset):
        url = self.API_URL + self.GET_QUOTE + asset.name
        asset_quote = self.url_to_json(url)
        try:
            if asset_quote != 0:
                asset.buy = asset_quote['buy']
                asset.sell = asset_quote['sell']
        except KeyError:
            # rollback
            asset.buy = -1
            asset.sell = -1
        finally:
            return asset

    def quote_for_assets(self, assets):
        return [self.get_asset_quote(a) for a in assets
                if self.has_quote(self.get_asset_quote(a))]

    def get_assets(self):
        assets = self.get_asset_names()
        return self.quote_for_assets(assets)

    def get_asset_history(self, nombre, start_date, end_date):
        url = self.API_URL + self.GET_HISTORY + nombre + "/" + start_date + \
              "/" + end_date
        prices = self.url_to_json(url)
        if prices == 0:
            prices = {'error': True}
        return prices
