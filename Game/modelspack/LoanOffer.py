from django.db import models


class LoanOffer(models.Model):
    from Game.models import Wallet
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    loan = models.FloatField(null=False, default=-1)
    interest_rate = models.FloatField(null=False, default=-1)
    days = models.IntegerField(null=False, default=-1)

    @staticmethod
    def safe_save(wallet, loan, interest, days):
        if loan > wallet.liquid or loan < 0:
            return {'error': True,
                    'message': 'You have not enough liquid money available'}

        if interest > 100 or interest < 0:
            return {'error': True,
                    'message': 'The interest rate is not a valid percentage'}

        if days < 0:
            return {'error': True,
                    'message': 'The days amount cannot be negative'}

        LoanOffer.objects.create(loan=loan, interest_rate=interest,
                                 days=days, wallet=wallet).save()

        # TODO: descontar la cantidad de dinero del liquido de la cartera
        return {'error': False,
                'message': 'Your loan offer has been created succesfully',
                'loaned': loan,
                'available': wallet.liquid_with_loans}
