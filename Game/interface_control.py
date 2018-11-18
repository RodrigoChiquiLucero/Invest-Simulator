import urllib3.request
import json
import datetime as dt
from urllib3 import exceptions as urlex
from Game.periodictasks.search_alarms import AlarmSearch

DATE_FORMAT = '%Y-%m-%d'


def str_to_date(strdate):
    """
    parses given string to date using global date format
    :param strdate:
    :return date:
    """
    return dt.datetime.strptime(strdate, DATE_FORMAT)


class AssetComunication:
    GET_ASSETS = "getAvailableAssets/"
    GET_QUOTE = "getAssetMarketPrice/"
    GET_HISTORY = "getAssetHistory/"

    def __init__(self, url):
        self.API_URL = url
        self.alarm_search = AlarmSearch(acom=self)

    @staticmethod
    def has_quote(asset):
        """
        check if an asset has a valid quote
        :param asset:
        :return boolean:
        """
        return asset.buy != -1 and asset.sell != -1

    @staticmethod
    def url_to_json(url):
        """
        fetch json data from given url
        :param url:
        :return json_response if success, 0 otherwise:
        """
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
        """
        fetch from API all the available assets (only names)
        :return asset list:
        """
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
        """
        given an asset (only name is required)
        returns same asset with buy and sell price if both exists
        also searchs for alarms for the given asset.
        :param asset:
        :return asset:
        """
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
            self.alarm_search.search_for_alarms(asset=asset)
            return asset

    def get_asset_type(self, name):
        assets = self.get_asset_names()
        for a in assets:
            if name == a.name:
                return a.type
        return None

    def quote_for_assets(self, assets):
        """
        maps asset list (only names are required) with same assets with quote
        :param assets:
        :return asset list:
        """
        return [self.get_asset_quote(a) for a in assets if
                self.has_quote(self.get_asset_quote(a))]

    def get_assets(self):
        """
        fetches all the available assets with their respective quotes
        :return asset list:
        """
        assets = self.get_asset_names()
        return self.quote_for_assets(assets)

    def get_asset_history(self, nombre, start_date, end_date):
        """
        get all history for given asset
        :param nombre:
        :param start_date:
        :param end_date:
        :return dict [{day: DayString, sell: SELL_PRICE, buy: BUY_PRICE}]:
        """
        url = (self.API_URL + self.GET_HISTORY + nombre + "/" +
               start_date + "/" + end_date)
        prices = self.url_to_json(url)
        if prices == 0:
            prices = {'error': True}
        return prices
