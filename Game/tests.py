from django.test import TestCase
from Game import interface_control as ic
from Game.models import AssetStruct


class InterfaceControlTest(TestCase):

    def setUp(self):
        return
        # ic.API_URL = 'http://localhost:8000/tests/'

    def test_sanity(self):
        # search for the names
        assets_name = ic.get_asset_names()
        self.assertNotEqual(assets_name, [])

        # search for all info
        asset_info = [ic.get_asset_quote(a) for a in assets_name if ic.has_quote(ic.get_asset_quote(a))]
        self.assertNotEqual(asset_info, [])

        # dedicated full method
        assets_complete = ic.get_assets()
        self.assertNotEqual(assets_complete, [])

    def test_border(self):
        # ask for a quote of unexistent asset
        asset = AssetStruct(name="NONE", asset_type="NONE")
        quote = ic.get_asset_quote(asset)
        self.assertEqual(quote, asset)
        self.assertEqual(quote.buy, -1)
        self.assertEqual(quote.sell, -1)

        # ask for a quote of existent asset
        asset = AssetStruct(name="MARSHALL", asset_type="currency")
        quote = ic.get_asset_quote(asset)
        self.assertNotEqual(asset, quote)
        self.assertNotEqual(quote.buy, -1)
        self.assertNotEqual(quote.sell, -1)

