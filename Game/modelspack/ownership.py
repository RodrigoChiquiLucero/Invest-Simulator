from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import datetime


class Ownership(models.Model):
    from Game.models import Wallet, Asset
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    @staticmethod
    def safe_get(wallet, asset):
        """
        get a specific ownership, return None if it doesn't exists
        :param wallet, asset:
        :return Ownership
        """
        try:
            return Ownership.objects.get(wallet=wallet, asset=asset)
        except ObjectDoesNotExist:
            return None


class Transaction(models.Model):
    from Game.models import Wallet, Asset
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.DO_NOTHING)
    asset_price_buy = models.FloatField(null=False, default=-1)
    asset_price_sell = models.FloatField(null=False, default=-1)
    date = models.DateField(default=datetime.date.today)
    quantity = models.FloatField()
    is_purchase = models.BooleanField(null=False)

    @staticmethod
    def get_info(wallet):
        """
        search for all made transactions
        :param wallet:
        :return dict {transactions: [Transactions]}:
        """
        response = {}
        transactions = Transaction.objects.filter(wallet=wallet,
                                                  quantity__gt=0)
        response['transactions'] = transactions
        return response
