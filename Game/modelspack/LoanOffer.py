from django.db import models
from django.forms.models import model_to_dict


class LoanOffer(models.Model):
    from Game.models import Wallet
    lender = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    offered = models.FloatField(null=False, default=-1)
    interest_rate = models.FloatField(null=False, default=-1)
    days = models.IntegerField(null=False, default=-1)

    @property
    def to_json(self):
        json = model_to_dict(self)
        json['offered_with_loans'] = self.offered_with_loans
        return json

    @property
    def offered_with_loans(self):
        from Game.models import Loan
        loans = Loan.objects.filter(offer=self)
        return self.offered - sum(l.loaned for l in loans)

    @staticmethod
    def safe_save(wallet, loaned, interest, days):
        try:
            loaned = float(loaned)
            interest = float(interest)
            days = int(days)
        except ValueError:
            return {'error': True,
                    'message': 'Incorrect data value'}
        if loaned > wallet.liquid or loaned < 0:
            return {'error': True,
                    'message': 'You have not enough liquid money available'}
        if interest > 100 or interest < 0:
            return {'error': True,
                    'message': 'The interest rate is not a valid percentage'}
        if days < 0:
            return {'error': True,
                    'message': 'The days amount cannot be negative'}
        LoanOffer.objects.create(loaned=loaned, interest_rate=interest,
                                 days=days, lender=wallet).save()
        return {'error': False,
                'message': 'Your loan offer has been created succesfully',
                'loaned': loaned,
                'available': wallet.liquid_with_loans}
