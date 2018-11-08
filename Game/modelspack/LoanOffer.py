from django.db import models


class LoanOffer(models.Model):
    from Game.models import Wallet
    lender = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    loaned = models.FloatField(null=False, default=-1)
    interest_rate = models.FloatField(null=False, default=-1)
    days = models.IntegerField(null=False, default=-1)

    @staticmethod
    def safe_save(wallet, loan, interest, days):
        try:
            loan = float(loan)
            interest = float(interest)
            days = int(days)
        except ValueError:
            return {'error': True,
                    'message': 'Incorrect data value'}
        if loan > wallet.liquid or loan < 0:
            return {'error': True,
                    'message': 'You have not enough liquid money available'}
        if interest > 100 or interest < 0:
            return {'error': True,
                    'message': 'The interest rate is not a valid percentage'}
        if days < 0:
            return {'error': True,
                    'message': 'The days amount cannot be negative'}
        LoanOffer.objects.create(loaned=loan, interest_rate=interest,
                                 days=days, lender=wallet).save()
        return {'error': False,
                'message': 'Your loan offer has been created succesfully',
                'loaned': loan,
                'available': wallet.liquid_with_loans}
