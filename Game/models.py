from django.db import models
from django.contrib.auth.models import User
import Game.AssetInterfaceControl.interface_control as interface_control


class Asset(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=75)

    def get_info(self):
        # TODO: pedir informacion a la api
        return interface_control.get_asset_by_id(id=self.id)


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
