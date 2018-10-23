from django.test import TestCase
from django.contrib.auth.models import User
from Game.models import Wallet, Asset, Ownership
from Game.interface_control import AssetComunication as AComunication


class InterfaceControlTest(TestCase):

    def setUp(self):
        self.asset_communication = AComunication(
            'http://localhost:8000/simulations/')
        user = User.objects.create(username='test_user')
        Wallet.objects.create(user=user)

    def test_asset_communication_sanity(self):
        # search for the names
        assets_name = self.asset_communication.get_asset_names()
        self.assertNotEqual(assets_name, [])

        # search for all info
        asset_info = [self.asset_communication.get_asset_quote(a)
                      for a in assets_name
                      if self.asset_communication.has_quote(
                self.asset_communication.get_asset_quote(a))]
        self.assertNotEqual(asset_info, [])

        # dedasset_communicationated full method
        assets_complete = self.asset_communication.get_assets()
        self.assertNotEqual(assets_complete, [])

    def test_asset_communication_border(self):
        # ask for a quote of unexistent asset
        asset = Asset(name="NONE", type="NONE")
        quote = self.asset_communication.get_asset_quote(asset)
        self.assertEqual(quote.buy, -1)
        self.assertEqual(quote.sell, -1)

        # ask for a quote of existent asset
        asset = Asset(name="MARSHALL", type="currency")
        quote = self.asset_communication.get_asset_quote(asset)
        self.assertNotEqual(quote.buy, -1)
        self.assertNotEqual(quote.sell, -1)

    def test_wallet_sanity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_asset_names()

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
            self.asset_communication.get_asset_quote(asset_a),
            self.asset_communication.get_asset_quote(asset_c)]
        result_assets = response['assets']
        self.assertEqual(len(result_assets), len(expected_assets))

        for e, r in zip(expected_assets, result_assets):
            self.assertEqual(e.name, r.name)

    def test_wallet_buy(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 2.3

        asset_c = assets[3]
        asset_c.quantity = 1.4

        # buy assets
        wallet.buy_asset(asset_a)
        wallet.buy_asset(asset_c)

    def test_wallet_buy_border(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_asset_names()

        asset_a = assets[0]
        asset_a = Asset.objects.create(name=asset_a.name,
                                       type=asset_a.type)
        asset_a = self.asset_communication.get_asset_quote(asset_a)
        asset_a.quantity = 200000

        # buy assets
        wallet.buy_asset(asset_a)

    def test_wallet_sell(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 2.3

        asset_c = assets[3]
        asset_c.quantity = 1.4

        # sell assets
        wallet.sell_asset(asset_a)
        wallet.sell_asset(asset_c)

    def test_wallet_sell_border(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_asset_names()

        asset_a = assets[0]
        asset_a = Asset.objects.create(name=asset_a.name,
                                       type=asset_a.type)
        asset_a = self.asset_communication.get_asset_quote(asset_a)
        asset_a.quantity = 20000000

        # sell assets
        wallet.sell_asset(asset_a)
