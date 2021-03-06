from django.db import models
from datetime import datetime as dt
from datetime import timedelta
from django.forms.models import model_to_dict


class Loan(models.Model):
    """
    Represents a taken LoanOffer
    """
    from Game.models import Wallet, LoanOffer
    borrower = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    offer = models.ForeignKey(LoanOffer, on_delete=models.CASCADE)
    loaned = models.FloatField(null=False, default=-1)
    due_date = models.DateField()

    @property
    def get_total_to_pay(self):
        return self.loaned + (self.loaned * self.offer.interest_rate / 100)

    @property
    def to_json(self):
        """
        Returns self information inside json string
        :rtype: Json String
        """
        json = model_to_dict(self)
        offer_json = model_to_dict(self.offer)
        json['offer'] = offer_json
        return json

    def charge_borrower(self):
        """
        If the wallet that took the loan has enough money, collect the
        money owed and return True, else return False
        :rtype: bool
        """
        total = self.loaned + (self.loaned * self.offer.interest_rate / 100)
        if total > self.borrower.liquid_with_loans:
            return False
        self.borrower.liquid -= total
        self.offer.lender.liquid += total
        self.borrower.save()
        self.offer.lender.save()
        self.delete()
        return True

    @staticmethod
    def safe_save(borrower, offer, loaned):
        """
        Method to save the loan for a borrower, also give the borrower the
        loaned money
        :rtype: None
        """
        borrower.liquid += loaned
        borrower.save()
        due_date = dt.now() + timedelta(days=offer.days)
        Loan(borrower=borrower, offer=offer,
             loaned=loaned, due_date=due_date).save()
