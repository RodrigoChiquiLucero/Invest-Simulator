from django.core.mail import send_mail
from django.contrib.auth.models import User


class AlarmSearch:
    help = 'Periodic check for triggered alarms'

    def __init__(self, acom):
        self.message = ''
        self.acom = acom

    def print_success(self):
        print(self.message)
        self.message = ''

    def search_for_alarms(self, asset):
        from Game.models import Alarm

        alarms = Alarm.objects.filter(asset__name=asset.name)
        for a in alarms:
            self.trigger(a, asset)
        self.print_success()

    def trigger(self, alarm, asset):
        if not alarm.triggered:
            if alarm.trigger(asset):
                self.message += ('Alarm triggered for: ' + alarm.asset.name +
                                 '  with threshold: ' + str(alarm.threshold) +
                                 '  and type: ' + alarm.type + '\n')

                price = asset.__getattribute__(alarm.price)
                user = User.objects.get(wallet=alarm.wallet)
                email = user.email
                self.message += 'sending to mail: ' + email + '\n'

                alarm.triggered = True
                alarm.save()

                send_mail(
                    'Your alarm for asset ' +
                    alarm.asset.name + ' has been triggered',

                    'The asset ' + asset.name +
                    ' has reached the expected value of $' + str(
                        alarm.threshold) +
                    '\n\n' + asset.name +
                    '\nCurrent price: $' + str(price),
                    'invest.simulator.alarms@gmail.com',
                    [email],
                    fail_silently=False,
                )
        else:
            alarm.reactivate(asset)
