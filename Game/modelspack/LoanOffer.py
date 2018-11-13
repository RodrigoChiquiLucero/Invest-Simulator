from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict


class LoanOffer(models.Model):
    from Game.models import Wallet
    lender = models.ForeignKey(Wallet, on_delete=models.CASCADE)
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
    def safe_save(wallet, offered, interest, days):
        try:
            offered = float(offered)
            interest = float(interest)
            days = int(days)
        except ValueError:
            return {'error': True,
                    'message': 'Incorrect data value'}
        if offered > wallet.liquid or offered < 0:
            return {'error': True,
                    'message': 'You have not enough liquid money available'}
        if interest > 100 or interest < 0:
            return {'error': True,
                    'message': 'The interest rate is not a valid percentage'}
        if days < 1:
            return {'error': True,
                    'message': 'The days amount cannot be negative'}
        LoanOffer.objects.create(offered=offered, interest_rate=interest,
                                 days=days, lender=wallet).save()
        return {'error': False,
                'message': 'Your loan offer has been created succesfully',
                'loaned': offered,
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
    def safe_delete(lender, id):
        try:
            offered_loan = LoanOffer.objects.get(lender=lender, id=int(id))
            offered_loan.delete()
            return {'error': False,
                    'message': "Your offer has been deleted successfully"}
        except (ObjectDoesNotExist, ValueError):
            return {'error': True,
                    'message': 'An error ocurred while trying to '
                               'delete the offer'}

    @staticmethod
    def safe_modification(lender, id, new_offer):
        try:
            new_offer = float(new_offer)
            offered_loan = LoanOffer.objects.get(lender=lender, id=int(id))
        except ObjectDoesNotExist:
            return {'error': True,
                    'message': "This offer isn't yours"}
        except ValueError:
            return {'error': True,
                    'message': "Incorrect data"}

        if new_offer > offered_loan.offered:
            return {'error': True,
                    'message': "You haven't loaned that much money"}
        elif new_offer == offered_loan.offered:
            return LoanOffer.safe_delete(lender, id)
        else:
            offered_loan.offered -= new_offer
            offered_loan.save()
            return {'error': False,
                    'message': "Your offer has been changed successfully"}
