from django.db import models
from django.contrib.auth.models import User
from Game import interface_control as ic


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
    assets = models.ManyToManyField(Asset)
    liquid = models.FloatField(null=False)

    @staticmethod
    def get_info(user):
        info = {}
        wallets = Wallet.objects.filter(user=user)
        wa = wallets[0] if wallets else None
        if wa:
            info['liquid'] = wa.liquid
            asset_list = [a.as_struct() for a in wa.assets.all()]
            asset_list = ic.quote_for_assets(asset_list)
            info['assets'] = asset_list
            info['error'] = False
        else:
            info['error'] = True
        return info


class Transaction(models.Model):
    id = models.IntegerField(primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    asset_price = models.FloatField(null=False)
    date = models.DateField()
    quantity = models.IntegerField()
    is_purchase = models.BooleanField(null=False)
