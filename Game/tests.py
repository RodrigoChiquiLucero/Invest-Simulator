from django.test import TestCase
from django.contrib.auth.models import User
from Game.models import Wallet, Asset, Ownership, Loan, LoanOffer
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

        # expected results
        expected_money_result = 7680.0
        expected_ownership_result = [
            Ownership.objects.create(asset=asset_a, wallet=wallet,
                                     quantity=2.3),
            Ownership.objects.create(asset=asset_c, wallet=wallet,
                                     quantity=1.4)]

        # buy assets
        wallet.buy_asset(asset_a)
        wallet.buy_asset(asset_c)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_buy_border_quantity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 200000

        # expected results
        expected_money_result = 10000
        expected_ownership_result = []

        # buy assets
        wallet.buy_asset(asset_a)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_buy_border_nil_quantity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 0

        # expected results
        expected_money_result = 10000
        expected_ownership_result = []

        # buy assets
        wallet.buy_asset(asset_a)

        # check algorithm response
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))
        self.assertEqual(expected_money_result, wallet.liquid)

    def test_wallet_sell_asset_part(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_c = assets[3]

        # create and save transactions
        own1 = Ownership.objects.create(asset=asset_a, quantity=3,
                                        wallet=wallet)
        own2 = Ownership.objects.create(asset=asset_c, quantity=5,
                                        wallet=wallet)

        asset_a.quantity = 2.3
        asset_c.quantity = 1.4

        # expected results
        expected_money_result = 11152.8
        expected_asset_a_quantity = 0.7
        expected_asset_c_quantity = 3.6
        expected_ownership_result = [own1, own2]

        # sell assets
        wallet.sell_asset(asset_a)
        wallet.sell_asset(asset_c)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_asset_a_quantity,
                         Ownership.objects.all()[0].quantity)
        self.assertEqual(expected_asset_c_quantity,
                         Ownership.objects.all()[1].quantity)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_sell_asset_full(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 3

        asset_c = assets[3]
        asset_c.quantity = 5

        # create and save transactions
        Ownership.objects.create(asset=asset_a, quantity=3, wallet=wallet)
        Ownership.objects.create(asset=asset_c, quantity=5, wallet=wallet)

        # expected results
        expected_money_result = 11510.0
        expected_ownership_result = []

        # sell assets
        wallet.sell_asset(asset_a)
        wallet.sell_asset(asset_c)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_sell_border_quantity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()
        asset_a = assets[0]
        asset_a.quantity = 20000000

        # create and save transactions
        own = Ownership.objects.create(asset=asset_a, quantity=3,
                                       wallet=wallet)

        # expected results
        expected_money_result = 10000
        expected_ownership_result = [own]

        # sell assets
        wallet.sell_asset(asset_a)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_sell_border_nil_quantity(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 0

        # create and save transactions
        own = Ownership.objects.create(asset=asset_a, quantity=3,
                                       wallet=wallet)

        # expected results
        expected_money_result = 10000
        expected_ownership_result = [own]

        # sell assets
        wallet.sell_asset(asset_a)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_sell_border_ownership(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 2

        # expected results
        expected_money_result = 10000
        expected_ownership_result = []

        # sell assets
        wallet.sell_asset(asset_a)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_wallet_buy_then_sell(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save assets
        assets = self.asset_communication.get_assets()

        asset_a = assets[0]
        asset_a.quantity = 2

        # expected results
        expected_money_result = 10200
        expected_ownership_result = []

        wallet.buy_asset(asset_a)
        wallet.sell_asset(asset_a)

        # check algorithm response
        self.assertEqual(expected_money_result, wallet.liquid)
        self.assertEqual(expected_ownership_result,
                         list(Ownership.objects.all()))

    def test_offerloan_regular_values(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save a loan offer
        loanoffer = LoanOffer(lender=wallet, offered=1000,
                              interest_rate=2.0, days=10)

        # check object saves correctly.
        self.assertEqual(loanoffer.offered, 1000)
        self.assertEqual(loanoffer.lender, wallet)
        self.assertEqual(loanoffer.interest_rate, 2.0)
        self.assertEqual(loanoffer.days, 10)

    def test_offerloan_then_modify(self):
        # get user
        user = User.objects.get(username='test_user')
        wallet = Wallet.objects.get(user=user)

        # create and save a loan offer
        loanoffer = LoanOffer(lender=wallet, offered=1000,
                              interest_rate=2.0, days=10)
        loanoffer.save()

        # record previous money amount
        oldliq = wallet.liquid
        # modify loan
        res = LoanOffer.safe_modification(lender=wallet, id=str(loanoffer.id),
                                          new_offer=500)
        loanoffer = LoanOffer.objects.get(id=loanoffer.id)
        # check modification.
        self.assertEqual(res['error'], False)
        self.assertEqual(loanoffer.offered, 500)
        self.assertEqual(loanoffer.lender, wallet)
        self.assertEqual(loanoffer.interest_rate, 2.0)
        self.assertEqual(loanoffer.days, 10)

        # check user has its money back.
        self.assertEqual(wallet.liquid_with_loans, oldliq - 500)
