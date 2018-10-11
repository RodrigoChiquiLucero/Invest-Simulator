import urllib3.request
import json
from Game.models import AssetStruct

API_URL = "https://bbe401af-1ad7-417c-b32b-a823a6d34b03.mock.pstmn.io/"
GET_ASSETS = "getAvailableAssets/"
GET_QUOTE = "getAssetMarketPrice/?name="


def url_to_json(url):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager()
    res = http.request('GET', url)
    if res.status == 200:
        return json.loads(res.data.decode())
    else:
        return 0


def get_asset_names():
    url = API_URL + GET_ASSETS
    json_assets = url_to_json(url)
    if json_assets != 0:
        asset_list = []
        for a in json_assets:
            asset = AssetStruct(name=a['name'], asset_type=a['type'])
            asset_list.append(asset)
        return asset_list
    return []


def get_asset_quote(asset):
    url = API_URL + GET_QUOTE + asset.name
    asset_quote = url_to_json(url)
    if asset_quote != 0:
        asset.buy = asset_quote['buy']
        asset.sell = asset_quote['sell']
    return asset


def has_quote(asset):
    return asset.buy != -1 and asset.sell != -1


def get_assets():
    assets = get_asset_names()
    return [get_asset_quote(a) for a in assets if has_quote(get_asset_quote(a))]
