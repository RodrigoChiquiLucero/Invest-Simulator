from django.db import models
from django.contrib.auth.models import User
from Game import interface_control as ic
import datetime


# /*
# TODO: separar todos los modelos en archivos distintos
# */


class Asset(models.Model):
    name = models.CharField(max_length=75, primary_key=True)
    type = models.CharField(max_length=10)

    def as_struct(self):
        return ic.AssetStruct(name=self.name, asset_type=self.type)


class Wallet(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liquid = models.FloatField(null=False)

    @staticmethod
    def get_info(user):
        response = {}
        try:
            wallet = Wallet.objects.filter(user=user)[0]
            response['liquid'] = wallet.liquid
            value_wallet = wallet.liquid
            transactions = Transaction.objects.filter(wallet=wallet, is_purchase=True)
            assets = []
            for t in transactions:
                asset = ic.get_asset_quote(t.asset.as_struct())
                asset.quantity = t.quantity
                value_wallet += t.quantity * asset.sell
                assets.append(asset)
            response['assets'] = assets
            response['value_wallet'] = value_wallet
            response['error'] = False
        except IndexError:
            response['error'] = True
        return response


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    asset_price = models.FloatField(null=False)
    date = models.DateField(default=datetime.date.today)
    quantity = models.IntegerField()
    is_purchase = models.BooleanField(null=False)
