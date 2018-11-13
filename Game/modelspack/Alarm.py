from django.db import models
from Game.interface_control import AssetComunication as ACommunication
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class Alarm(models.Model):
    from Game.models import Wallet, Asset
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.TextField(null=False, default='up')
    threshold = models.FloatField(null=False, default=-1)
    type = models.TextField(null=False, default='up')
    triggered = models.BooleanField(null=False, default=False)
    old_price = models.FloatField(null=False, default=-1)

    def trigger(self):
        acom = ACommunication(settings.API_URL)
        asset = acom.get_asset_quote(self.asset)

        if not asset.is_valid():
            return False

        if self.type == 'up':
            return asset.__getattribute__(self.price) > self.threshold
        else:
            return asset.__getattribute__(self.price) < self.threshold

    def reactivate(self):
        acom = ACommunication(settings.API_URL)
        asset = acom.get_asset_quote(self.asset)
        if self.type == 'up':
            self.triggered = asset.__getattribute__(
                self.price) >= self.threshold
        else:
            self.triggered = asset.__getattribute__(
                self.price) <= self.threshold
        self.save()

    @staticmethod
    def safe_get(wallet, asset, price, type):
        try:
            return Alarm.objects.get(wallet=wallet, asset=asset, price=price,
                                     type=type)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def safe_save(wallet, aname, threshold, atype, price):
        from Game.models import Asset
        acom = ACommunication(settings.API_URL)
        asset = Asset.create_if_not_exists(aname)
        if not asset:
            return {'error': True, 'message': 'Non existing asset'}

        asset = acom.get_asset_quote(asset)

        if Alarm.safe_get(wallet, asset, price, atype):
            return {'error': True,
                    'message': 'You already have an alarm on this asset'}

        Alarm.objects.create(wallet=wallet, asset=asset,
                             price=price,
                             old_price=asset.__getattribute__(price),
                             threshold=threshold, type=atype).save()
        return {'error': False,
                'message': 'Your alarm has been set successfully!'}

    @staticmethod
    def get_info(wallet):
        alarms = Alarm.objects.filter(wallet=wallet)
        if not alarms:
            return {'error': True, 'message': "You don't have any alarm set"}
        else:
            return {'error': False, 'alarms': alarms}

    @staticmethod
    def safe_delete(wallet, name, atype, price):
        from Game.models import Asset
        asset = Asset.objects.get(name=name)
        alarm = Alarm.objects.get(asset=asset, wallet=wallet,
                                  type=atype, price=price)
        alarm.delete()
