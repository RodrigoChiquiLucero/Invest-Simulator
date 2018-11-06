from django.db import models


class LoanOffer(models.Model):
    from Game.models import Wallet
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    loan = models.FloatField(null=False, default=-1)
    interest_rate = models.FloatField(null=False, default=-1)
    days = models.IntegerField(null=False, default=-1)
