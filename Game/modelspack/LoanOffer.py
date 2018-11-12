from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class LoanOffer(models.Model):
    from Game.models import Wallet
    lender = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    loaned = models.FloatField(null=False, default=-1)
    interest_rate = models.FloatField(null=False, default=-1)
    days = models.IntegerField(null=False, default=-1)

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
                'message': 'Your loan offer has been created successfully',
                'loaned': loaned,
                'available': wallet.liquid_with_loans}

    @staticmethod
    def safe_get(lender):
        try:
            return LoanOffer.objects.get(lender=lender)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_info(lender):
        offered_loans = LoanOffer.objects.filter(lender=lender,
                                                 quantity__gt=0)
        if not offered_loans:
            return {'error': True,
                    'message': "You don't have any loan offer set"}
        else:
            return {'error': False, 'offered_loans': offered_loans}

    @staticmethod
    def safe_delete(lender, loaned, interest_rate, days):
        offered_loans = LoanOffer.objects.get(lender=lender, loaned=loaned,
                                              interest_rate=interest_rate,
                                              days=days)
        offered_loans.delete()

    @staticmethod
    def safe_modification(lender, loaned, interest_rate, days, new_loan):
        from Game.models import Wallet
        print("AAA")
        print(loaned)
        print(new_loan)
        print("AAA")
        if float(new_loan) > float(loaned):
            return {'error': True,
                    'message': "You haven't loaned that much money"}
        else:
            offered_loans = LoanOffer.objects.get(lender=lender, loaned=loaned,
                                                  interest_rate=interest_rate,
                                                  days=days)
            withdrawn_money = offered_loans.loaned - float(new_loan)
            offered_loans.loaned = withdrawn_money
            offered_loans.save()
