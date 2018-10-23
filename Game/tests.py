from django.test import TestCase
from django.contrib.auth.models import User
from Game.models import Wallet, Asset, Ownership
from Game.interface_control import AssetComunication as AComunication
from Game import interface_control as ic
from Game.models import Asset
from django.conf import settings


class InterfaceControlTest(TestCase):

    def setUp(self):
        self.asset_comunication = AComunication(
            'http://localhost:8000/simulations/')
        user = User.objects.create(username='test_user')
        Wallet.objects.create(user=user)

    def test_asset_comunication_sanity(self):
        # search for the names
        assets_name = self.asset_comunication.get_asset_names()
        self.assertNotEqual(assets_name, [])

        # search for all info
        asset_info = [self.asset_comunication.get_asset_quote(a)
                      for a in assets_name
                      if self.asset_comunication.has_quote(
                self.asset_comunication.get_asset_quote(a))]
        self.assertNotEqual(asset_info, [])

        # dedasset_comunicationated full method
        assets_complete = self.asset_comunication.get_assets()
        self.assertNotEqual(assets_complete, [])

    def test_asset_comunication_border(self):
        # ask for a quote of unexistent asset
        asset = Asset(name="NONE", type="NONE")
        quote = self.asset_comunication.get_asset_quote(asset)
        self.assertEqual(quote.buy, -1)
        self.assertEqual(quote.sell, -1)

        # ask for a quote of existent asset
        asset = Asset(name="MARSHALL", type="currency")
        quote = self.asset_comunication.get_asset_quote(asset)
        self.assertNotEqual(quote.buy, -1)
        self.assertNotEqual(quote.sell, -1)

    def test_wallet_sanity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_comunication.get_asset_names()

        asset_a = assets[0]
        asset_a = Asset.objects.create(name=asset_a.name, type=asset_a.type)
        asset_c = assets[3]
        asset_c = Asset.objects.create(name=asset_c.name, type=asset_c.type)

        # create and save transactions
        Ownership.objects.create(asset=asset_a, quantity=3, wallet=wallet)
        Ownership.objects.create(asset=asset_c, quantity=5, wallet=wallet)

        # check algorithm response
        response = Wallet.get_info(user)
        self.assertFalse(response['error'])
        expected_assets = [
            self.asset_comunication.get_asset_quote(asset_a),
            self.asset_comunication.get_asset_quote(asset_c)]
        result_assets = response['assets']
        self.assertEqual(len(result_assets), len(expected_assets))

        for e, r in zip(expected_assets, result_assets):
            self.assertEqual(e.name, r.name)

    def test_wallet_buy(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # set communication
        asset_comms = ic.AssetComunication(settings.API_URL)

        # create and save assets
        assets = self.asset_comunication.get_asset_names()

        asset_a = assets[0]
        asset_a = Asset.objects.create(name=asset_a.name, type=asset_a.type)
        asset_a = asset_comms.get_asset_quote(asset_a)
        asset_a.quantity = 2.3

        asset_c = assets[3]
        asset_c = Asset.objects.create(name=asset_c.name, type=asset_c.type)
        asset_c = asset_comms.get_asset_quote(asset_c)
        asset_c.quantity = 1.4

        # check wallet money
        print(wallet.liquid)

        # buy assets
        wallet.buy_asset(asset_a)
        wallet.buy_asset(asset_c)

        # check money again
        print(wallet.liquid)

    def test_wallet_sell(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # set communication
        asset_comms = ic.AssetComunication(settings.API_URL)

        # create and save assets
        assets = self.asset_comunication.get_asset_names()

        asset_a = assets[0]
        asset_a = Asset.objects.create(name=asset_a.name,
                                       type=asset_a.type)
        asset_a = asset_comms.get_asset_quote(asset_a)
        asset_a.quantity = 2.3

        asset_c = assets[3]
        asset_c = Asset.objects.create(name=asset_c.name,
                                       type=asset_c.type)
        asset_c = asset_comms.get_asset_quote(asset_c)
        asset_c.quantity = 1.4

        # check wallet money
        print(wallet.liquid)

        # sell assets
        wallet.sell_asset(asset_a)
        wallet.sell_asset(asset_c)

        # check money again
        print(wallet.liquid)

