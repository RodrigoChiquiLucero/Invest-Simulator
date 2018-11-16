from django.db import models
from django.contrib.auth.models import User
from Game.interface_control import AssetComunication as ACommunication
import datetime
from django.conf import settings


class Wallet(models.Model):
    from Game.models import Asset
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liquid = models.FloatField(null=False, default=10000)
    assets = models.ManyToManyField(Asset, through='Ownership')
    image = models.ImageField(upload_to='profile_image',
                              default='profile_image/no_image.jpg')

    @property
    def liquid_with_loans(self):
        from Game.models import LoanOffer
        loan_offers = LoanOffer.objects.filter(lender=self)
        return self.liquid - sum(l.offered for l in loan_offers)

    @staticmethod
    def get_info(user):
        from Game.models import Ownership
        """
        full wallet info given user
        :param user:
        :return dict {assets: [Asset], value_wallet: Float, error: Bool}
        """
        response = {}
        wallet = Wallet.objects.get(user=user)
        response['liquid'] = wallet.liquid_with_loans
        value_wallet = wallet.liquid_with_loans
        ownerships = Ownership.objects.filter(wallet=wallet, quantity__gt=0)
        assets = []
        asset_communication = ACommunication(settings.API_URL)
        for o in ownerships:
            asset = asset_communication.get_asset_quote(o.asset)
            asset.quantity = o.quantity
            value_wallet += o.quantity * asset.sell
            assets.append(asset)
        response['assets'] = assets
        response['value_wallet'] = value_wallet
        response['error'] = False
        return response

    def buy_asset(self, asset):
        from Game.models import Asset, Transaction
        """
        add an asset to the user wallet and add the transaction to user history
        :param asset:
        :return: dict {error: Bool, message: String}
        """
        asset_comms = ACommunication(settings.API_URL)
        asset = asset_comms.get_asset_quote(asset)
        total = (asset.buy * asset.quantity)
        buy = asset.buy
        sell = asset.sell
        quantity = asset.quantity
        name = asset.name
        type = asset.type

        if quantity <= 0:
            return {"error": True,
                    "message": "You need to buy at least one asset"}

        if self.liquid_with_loans >= total:
            asset = Asset.safe_get(name=asset.name)
            # if not asset then create one
            if not asset:
                asset = Asset(name=name,
                              type=type)
                asset.save()

            asset.quantity = quantity
            asset.buy = buy
            asset.sell = sell

            self.create_or_update_ownership(asset, quantity)

            Transaction(wallet=self, asset=asset, asset_price_buy=asset.buy,
                        asset_price_sell=asset.sell,
                        date=datetime.datetime.now(), quantity=quantity,
                        is_purchase=True, visibility=False).save()

            self.liquid -= total
            self.liquid = round(self.liquid, 3)
            self.save()
            return {"error": False, "message": "Purchase has been successful"}
        else:
            return {"error": True, "message": "Not enough cash"}

    def sell_asset(self, asset):
        from Game.models import Ownership, Transaction
        """
        remove an asset to the user wallet and
        add the transaction to user history.
        :param asset:
        :return: dict {error: Bool, message: String}
        """
        asset_comms = ACommunication(settings.API_URL)
        asset = asset_comms.get_asset_quote(asset)
        total = (asset.sell * asset.quantity)
        quantity = asset.quantity

        if quantity <= 0:
            return {"error": True,
                    "message": "You need to sell at least one asset"}

        ownership = Ownership.safe_get(wallet=self, asset=asset)
        if not ownership:
            return {"error": True, "message": "You do not own this asset"}

        if asset.quantity > ownership.quantity:
            return {"error": True, "message": "Not enough assets"}

        if asset.quantity == ownership.quantity:
            ownership.delete()
        else:
            ownership.quantity -= asset.quantity
            ownership.quantity = round(ownership.quantity, 3)
            ownership.save()

        Transaction(wallet=self, asset=asset, asset_price_buy=asset.buy,
                    asset_price_sell=asset.sell,
                    date=datetime.datetime.now(), quantity=asset.quantity,
                    is_purchase=False, visibility=False).save()

        self.liquid += total
        ownership.quantity = round(self.liquid, 3)
        self.save()
        return {"error": False, "message": "Sale has been succesfull"}

    def create_or_update_ownership(self, asset, quantity):
        from Game.models import Ownership
        ownership = Ownership.safe_get(wallet=self, asset=asset)
        if not ownership:
            ownership = Ownership(asset=asset, wallet=self,
                                  quantity=quantity)
        else:
            ownership.quantity += quantity
            ownership.quantity = round(ownership.quantity, 3)
        ownership.save()

    def delete_for_loan(self):
        taken = list(self.loan_set.all())
        ownerships = list(self.ownership_set.all())
        total_loaned = sum([lo.loaned for lo in taken])
        for lo in taken:
            percentage = total_loaned / (lo.loaned * 10)
            lo.offer.lender.liquid += self.liquid * percentage
            lo.offer.lender.save()
            for o in ownerships:
                lo.offer.lender.create_or_update_ownership(
                    o.asset, o.quantity * percentage)
        self.user.delete()
        self.delete()
