from django.core.mail import send_mail
from django.contrib.auth.models import User


class AlarmSearch:
    help = 'Periodic check for triggered alarms'

    def __init__(self, acom):
        self.BEGIN = \
            '--------------------- ALARM SEARCH ---------------------\n'
        self.END = \
            '------------------- END ALARM SEARCH -------------------\n'
        self.message = ''
        self.acom = acom

    def print_success(self):
        print(self.BEGIN + self.message + '\n' + self.END)
        self.message = ''

    def search_for_alarms(self):
        from Game.models import Alarm
        self.message += 'Searching for triggered alarms \n'

        alarms = Alarm.objects.all()
        for a in alarms:
            self.trigger(a)
        self.print_success()

    def trigger(self, alarm):
        if not alarm.triggered:
            if alarm.trigger():
                self.message += ('Alarm triggered for: ' + alarm.asset.name +
                                 '  with threshold: ' + str(alarm.threshold) +
                                 '  and type: ' + alarm.type + '\n')

                asset = self.acom.get_asset_quote(alarm.asset)
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
            alarm.reactivate()
