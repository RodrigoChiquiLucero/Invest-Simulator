import urllib3.request
import json

API_URL = "http://localhost:8000/tests/"
GET_ASSETS = "getAvailableAssets/"
GET_QUOTE = "getAssetMarketPrice/"


class AssetStruct:
    def __init__(self, name, asset_type, sell=-1, buy=-1, quantity=1):
        self.name = name
        self.type = asset_type
        self.sell = sell
        self.buy = buy
        self.quantity = quantity


def url_to_json(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    res = http.request('GET', url)
    if res.status == 200:
        return json.loads(res.data.decode())
    else:
        # notify error
        return 0


def get_asset_names():
    url = API_URL + GET_ASSETS
    json_assets = url_to_json(url)
    asset_list = []
    try:
        if json_assets != 0:
            json_assets = json_assets['availableAssets']
            for a in json_assets:
                asset = AssetStruct(name=a['name'], asset_type=a['type'])
                asset_list.append(asset)
            return asset_list
    except KeyError:
        # rollback
        asset_list = []
    finally:
        return asset_list


def get_asset_quote(asset):
    url = API_URL + GET_QUOTE + asset.name
    asset_quote = url_to_json(url)
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


def has_quote(asset):
    return asset.buy != -1 and asset.sell != -1


def quote_for_assets(assets):
    return [get_asset_quote(a) for a in assets if has_quote(get_asset_quote(a))]


def get_assets():
    assets = get_asset_names()
    return quote_for_assets(assets)
