from django.db import models


class Notification(models.Model):
    from Game.models import Wallet
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    message_short = models.TextField(null=False, default='')
    message_large = models.TextField(null=False, default='')
    times = models.IntegerField(null=False, default=3)

    @staticmethod
    def notifity(wallet):
        try:
            notif = Notification.objects.filter(wallet=wallet)[0]
            notif.times -= 1
            if notif.times == 0:
                notif.delete()
            else:
                notif.save()
            return {'must_notifiy': True,
                    'message_short': notif.message_short,
                    'message_large': notif.message_large}
        except IndexError:
            return {'must_notifiy': False}
