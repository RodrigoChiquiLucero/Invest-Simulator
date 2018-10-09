import urllib3.request
import json

API_URL = "http://c901b5d3-2510-4c5b-b7ad-c6a4b0b52267.mock.pstmn.io"


class AssetStruct:
    def __init__(self, id, name, sell, buy):
        self.id = id
        self.name = name
        self.sell = sell
        self.buy = buy


def get_assets_json():
    http = urllib3.PoolManager()
    response = http.request('GET', API_URL + '/assets/')
    # TODO : manejar errores en caso de que la api no traiga nada
    if response.status == 200:
        return json.loads(response.data.decode())
    else:
        return 0


def get_assets():
    json_assets = get_assets_json()
    assets = []
    if json_assets == 0:
        return assets
    for a in json_assets:
        asset = AssetStruct(int(a['id']), a['name'], float(a['sell']), float(a['buy']))
        assets.append(asset)
    return assets


def get_asset_by_id(id):
    json_assets = get_assets_json()
    for a in json_assets:
        if int(a['id']) == id:
            return AssetStruct(int(a['id']), a['name'], float(a['sell']), float(a['buy']))
