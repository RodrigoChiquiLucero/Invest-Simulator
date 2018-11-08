from django.db import models
from datetime import datetime as dt
from datetime import timedelta


class Loan(models.Model):
    from Game.models import Wallet, LoanOffer
    borrower = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    offer = models.ForeignKey(LoanOffer, on_delete=models.DO_NOTHING)
    loaned = models.FloatField(null=False, default=-1)
    due_date = models.DateField()

    @staticmethod
    def safe_save(borrower, offer, loaned):
        # calculate the due date with LoanOffer.days
        due_date = dt.now() + timedelta(days=offer.days)
        Loan(borrower=borrower, offer=offer,
             loaned=loaned, due_date=due_date).save()
