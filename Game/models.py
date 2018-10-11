from django.db import models
from django.contrib.auth.models import User


class AssetStruct:
    def __init__(self, name, asset_type, sell=0, buy=0):
        self.name = name
        self.type = asset_type
        self.sell = sell
        self.buy = buy


class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=75)
    type = models.CharField(max_length=10)


class Wallet(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assets = models.ManyToManyField(Asset)
    liquid = models.FloatField(null=False)


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_price = models.FloatField(null=False)
    date = models.DateField()
    quantity = models.IntegerField()
    is_purchase = models.BooleanField(null=False)
