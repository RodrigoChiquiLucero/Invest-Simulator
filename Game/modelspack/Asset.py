from django.db import models
from Game.interface_control import AssetComunication as ACommunication
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


class Asset(models.Model):
    name = models.CharField(max_length=75, primary_key=True, unique=True)
    type = models.CharField(max_length=10)
    # non persistent data
    buy = -1
    sell = -1
    quantity = -1
    prices_quantiles = -1

    def is_valid(self):
        """
        Checks if any of the buy/sell price is -1
        :rtype: bool
        """
        return self.buy != -1 and self.sell != -1

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "buy": self.buy,
            "sell": self.sell,
            "quantity": self.quantity,
            "quantiles": self.prices_quantiles,
        }

    @staticmethod
    def create_if_not_exists(name):
        """
        Look for an asset buy name, if asset doesn't exists, it creates it.
        :rtype: Asset
        """
        asset = Asset.safe_get(name)
        if not asset:
            asset_comms = ACommunication(settings.API_URL)
            type = asset_comms.get_asset_type(name)
            if not type:
                return None
            asset = Asset.objects.create(name=name, type=type)
            asset.save()
        return asset

    @staticmethod
    def safe_get(name):
        """
        Returns asset if exists, None otherwise
        :rtype: Asset
        """
        try:
            return Asset.objects.get(name=name)
        except ObjectDoesNotExist:
            return None
