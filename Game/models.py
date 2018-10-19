from django.db import models
from django.contrib.auth.models import User
from Game.interface_control import AssetComunication as ACommunication
from Game import interface_control as ic
import datetime
from django.conf import settings


# /*
# TODO: separar todos los modelos en archivos distintos
# */


class Asset(models.Model):
    name = models.CharField(max_length=75, primary_key=True, unique=True)
    type = models.CharField(max_length=10)

    @staticmethod
    def from_struct(struct):
        return Asset(name=struct.name, type=struct.type)

    def as_struct(self):
        return ic.AssetStruct(name=self.name, asset_type=self.type)


class Wallet(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liquid = models.FloatField(null=False, default=10000)
    assets = models.ManyToManyField(Asset, through='Ownership')
    image = models.ImageField(upload_to='profile_image', default='profile_image/no_image.jpg')

    @staticmethod
    def get_info(user):
        response = {}
        wallet = Wallet.objects.get(user=user)
        response['liquid'] = wallet.liquid
        value_wallet = wallet.liquid
        ownerships = Ownership.objects.filter(wallet=wallet, quantity__gt=0)
        assets = []
        asset_communication = ACommunication(settings.API_URL)
        for o in ownerships:
            asset = asset_communication.get_asset_quote(o.asset.as_struct())
            asset.quantity = o.quantity
            value_wallet += o.quantity * asset.sell
            assets.append(asset)
        response['assets'] = assets
        response['value_wallet'] = value_wallet
        response['error'] = False
        return response


class Ownership(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    asset_price = models.FloatField(null=False)
    date = models.DateField(default=datetime.date.today)
    quantity = models.IntegerField()
    is_purchase = models.BooleanField(null=False)

    @staticmethod
    def get_info(wallet):
        response = {}
        transactions = Transaction.objects.filter(wallet=wallet, quantity__gt=0)
        response['transactions'] = transactions
        response['error'] = False
        return response

