from django.db import models
from datetime import datetime as dt
from datetime import timedelta
from django.forms.models import model_to_dict


class Loan(models.Model):
    from Game.models import Wallet, LoanOffer
    borrower = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    offer = models.ForeignKey(LoanOffer, on_delete=models.DO_NOTHING)
    loaned = models.FloatField(null=False, default=-1)
    due_date = models.DateField()

    @property
    def to_json(self):
        json = model_to_dict(self)
        offer_json = model_to_dict(self.offer)
        json['offer'] = offer_json
        return json

    @staticmethod
    def safe_save(borrower, offer, loaned):
        # calculate the due date with LoanOffer.days
        borrower.liquid += loaned
        borrower.save()
        due_date = dt.now() + timedelta(days=offer.days)
        Loan(borrower=borrower, offer=offer,
             loaned=loaned, due_date=due_date).save()
